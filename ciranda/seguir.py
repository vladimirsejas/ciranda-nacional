"""Leitura e importação isolada de catálogos publicados por outra instância."""
import http.client
import ipaddress
import json
import os
import re
import socket
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from ciranda.servico import CAMPOS_PERMITIDOS

IDENTIFICADOR_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_RESPOSTA_BYTES = 2 * 1024 * 1024
MAX_SERVICOS = 500
MAX_CAMPO_TEXTO = 4000


def _resolver_endereco_publico(url):
    """Resolve o host e rejeita localhost, IP literal e qualquer IP não global."""
    partes = urlparse(url)
    if partes.scheme != "https" or not partes.hostname:
        raise ValueError("O endereço da instância deve usar HTTPS.")
    if partes.username or partes.password or partes.query or partes.fragment:
        raise ValueError("O endereço não pode conter usuário, senha, consulta ou fragmento.")
    host = partes.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError("Endereços localhost ou de rede local não são permitidos.")
    if re.fullmatch(r"[0-9.]+", host):
        raise ValueError("Endereços IP numéricos não são permitidos; use um nome público.")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("Endereços IP numéricos não são permitidos; use um nome público.")
    try:
        porta = partes.port or 443
    except ValueError as erro:
        raise ValueError("O endereço contém uma porta inválida.") from erro
    try:
        respostas = socket.getaddrinfo(host, porta, type=socket.SOCK_STREAM)
    except OSError as erro:
        raise ValueError("Não foi possível resolver o endereço público: {}".format(erro)) from erro
    ips = []
    for resposta in respostas:
        ip_texto = resposta[4][0].split("%", 1)[0]
        try:
            endereco_ip = ipaddress.ip_address(ip_texto)
        except ValueError as erro:
            raise ValueError("O DNS retornou um endereço IP inválido.") from erro
        if not endereco_ip.is_global:
            raise ValueError("O endereço foi recusado porque resolve para IP privado, local ou reservado.")
        if ip_texto not in ips:
            ips.append(ip_texto)
    if not ips:
        raise ValueError("O endereço não possui IP público válido.")
    return host, porta, ips[0]


def _baixar_corpo_https(url):
    """Baixa uma resposta HTTPS com IP fixado após validação DNS e limite de bytes."""
    host, porta, ip_publico = _resolver_endereco_publico(url)
    partes = urlparse(url)
    caminho = partes.path or "/"
    conexao = http.client.HTTPSConnection(host, port=porta, timeout=15)
    # Evita uma segunda resolução DNS: a conexão usa exatamente o IP público validado acima.
    conexao._create_connection = lambda _address, timeout, source_address: socket.create_connection(
        (ip_publico, porta), timeout, source_address
    )
    try:
        conexao.request("GET", caminho, headers={
            "Accept": "application/activity+json, application/json",
            "Connection": "close",
        })
        resposta = conexao.getresponse()
        if resposta.status != 200:
            raise ValueError("A instância respondeu com HTTP {}.".format(resposta.status))
        tamanho = resposta.getheader("Content-Length")
        if tamanho:
            try:
                tamanho = int(tamanho)
            except (TypeError, ValueError) as erro:
                raise ValueError("A resposta informou um tamanho inválido.") from erro
            if tamanho < 0 or tamanho > MAX_RESPOSTA_BYTES:
                raise ValueError("Resposta excede o limite de 2 MB ou informa tamanho inválido.")
        corpo = resposta.read(MAX_RESPOSTA_BYTES + 1)
        if len(corpo) > MAX_RESPOSTA_BYTES:
            raise ValueError("Resposta excede o limite de 2 MB.")
        return corpo
    except (OSError, http.client.HTTPException) as erro:
        raise ValueError("Falha ao consultar a instância por HTTPS: {}".format(erro)) from erro
    finally:
        conexao.close()


def _ler_json_local_ou_url(origem, nome):
    caminho = Path(str(origem))
    if caminho.is_dir():
        arquivo = caminho / nome
        try:
            conteudo = arquivo.read_bytes()
        except FileNotFoundError as erro:
            raise ValueError("Arquivo obrigatório não encontrado: {}".format(arquivo)) from erro
        if len(conteudo) > MAX_RESPOSTA_BYTES:
            raise ValueError("Arquivo excede o limite de 2 MB: {}".format(arquivo))
    else:
        base = str(origem).rstrip("/")
        url = base + "/" + nome
        conteudo = _baixar_corpo_https(url)
    try:
        return json.loads(conteudo.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as erro:
        raise ValueError("JSON inválido em '{}': {}".format(nome, erro)) from erro


def _validar_texto(valor, campo):
    if not isinstance(valor, str):
        raise ValueError("O campo '{}' deve conter texto.".format(campo))
    if len(valor) > MAX_CAMPO_TEXTO:
        raise ValueError("O campo '{}' excede o limite de {} caracteres.".format(campo, MAX_CAMPO_TEXTO))


def _validar_todos_os_textos(valor, caminho="documento"):
    """Aplica o limite de texto a todos os valores e chaves de um JSON recebido."""
    if isinstance(valor, str):
        _validar_texto(valor, caminho)
    elif isinstance(valor, dict):
        for chave, item in valor.items():
            _validar_texto(chave, caminho + ".chave")
            _validar_todos_os_textos(item, caminho + "." + chave)
    elif isinstance(valor, list):
        for indice, item in enumerate(valor):
            _validar_todos_os_textos(item, "{}[{}]".format(caminho, indice))


def _ler_publicacao(origem):
    local = Path(str(origem)).is_dir()
    if local:
        actor = _ler_json_local_ou_url(origem, "actor.json")
        outbox = _ler_json_local_ou_url(origem, "outbox.json")
    else:
        base = str(origem).rstrip("/")
        actor = _ler_json_local_ou_url(base, "actor.json")
        outbox = _ler_json_local_ou_url(base, "outbox.json")
    if not isinstance(actor, dict) or actor.get("type") != "Organization":
        raise ValueError("Perfil inválido: esperado um perfil Organization.")
    if not isinstance(outbox, dict) or outbox.get("type") != "OrderedCollection":
        raise ValueError("Lista de publicações inválida: esperado OrderedCollection.")
    atividades = outbox.get("orderedItems")
    if not isinstance(atividades, list):
        raise ValueError("Lista de publicações inválida: 'orderedItems' deve ser uma lista.")
    if len(atividades) > MAX_SERVICOS:
        raise ValueError("A instância excedeu o limite de {} serviços.".format(MAX_SERVICOS))
    try:
        _validar_todos_os_textos(actor, "perfil")
        _validar_todos_os_textos(outbox, "lista de publicações")
    except RecursionError as erro:
        raise ValueError("O JSON publicado possui estrutura profunda demais.") from erro
    for campo in ("id", "preferredUsername", "name", "summary", "url"):
        _validar_texto(actor.get(campo, ""), "perfil." + campo)
    identificador = actor.get("preferredUsername")
    if not isinstance(identificador, str) or not IDENTIFICADOR_RE.fullmatch(identificador):
        raise ValueError("Perfil inválido: identificador da instância ausente ou inválido.")
    if not isinstance(actor.get("id"), str):
        raise ValueError("Perfil inválido: endereço público do perfil ausente ou inválido.")
    endereco_perfil = urlparse(actor["id"])
    if (endereco_perfil.scheme != "https" or not endereco_perfil.hostname
            or endereco_perfil.username or endereco_perfil.password
            or endereco_perfil.query or endereco_perfil.fragment
            or not endereco_perfil.path.endswith("/actor.json")):
        raise ValueError("Perfil inválido: use URL HTTPS pública terminada em /actor.json.")
    if not local:
        host_solicitado = urlparse(str(origem)).hostname
        if endereco_perfil.hostname != host_solicitado:
            raise ValueError("O perfil publicado não corresponde ao domínio consultado.")
    servicos = []
    for indice, atividade in enumerate(atividades, start=1):
        if not isinstance(atividade, dict) or atividade.get("type") != "Create":
            raise ValueError("Publicação {} inválida: atividade Create esperada.".format(indice))
        if atividade.get("actor") != actor["id"]:
            raise ValueError("Publicação {} tem origem diferente do perfil.".format(indice))
        objeto = atividade.get("object")
        documento = objeto.get("ciranda:servico") if isinstance(objeto, dict) else None
        if not isinstance(documento, dict):
            raise ValueError("Publicação {} não contém documento de serviço Ciranda.".format(indice))
        if set(documento) - set(CAMPOS_PERMITIDOS):
            raise ValueError("Publicação {} contém campos não permitidos.".format(indice))
        for campo, valor in documento.items():
            if campo == "a_confirmar":
                if not isinstance(valor, bool):
                    raise ValueError("Publicação {} tem marca a_confirmar inválida.".format(indice))
            else:
                _validar_texto(valor, "servico.{}".format(campo))
        if documento.get("origem_instancia") != identificador:
            raise ValueError("Publicação {} informa origem diferente da instância publicadora.".format(indice))
        if not documento.get("id") or not documento.get("data_conferencia"):
            raise ValueError("Publicação {} não informa id ou data de conferência.".format(indice))
        servicos.append(documento)
    return actor, servicos


def _montar_importacao(actor, servicos):
    identificador = actor["preferredUsername"]
    importado_em = datetime.now(timezone.utc).isoformat()
    return {
        "instancia": {
            "identificador": identificador,
            "nome": actor.get("name", identificador),
            "endereco_publico": actor["id"].rsplit("/actor.json", 1)[0],
        },
        "importado_em": importado_em,
        "servicos": [
            {
                "origem": identificador,
                "data_conferencia_publicada": servico["data_conferencia"],
                "data_importacao": importado_em,
                "verificado_localmente": False,
                "servico": servico,
            }
            for servico in servicos
        ],
    }


def _gravar_sem_sobrescrever(arquivo, dados):
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    descritor = os.open(str(arquivo), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(descritor, "w", encoding="utf-8") as destino:
            json.dump(dados, destino, ensure_ascii=False, indent=2)
            destino.write("\n")
            destino.flush()
            os.fsync(destino.fileno())
    except Exception:
        try:
            arquivo.unlink()
        except OSError:
            pass
        raise


def seguir_instancia(endereco, pasta_importados="ciranda/importados"):
    """Importa serviços em arquivo separado; nunca altera o catálogo local nem sobrescreve importação."""
    actor, servicos = _ler_publicacao(endereco)
    identificador = actor["preferredUsername"]
    arquivo = Path(pasta_importados) / (identificador + ".json")
    dados = _montar_importacao(actor, servicos)
    _gravar_sem_sobrescrever(arquivo, dados)
    return {"arquivo": str(arquivo), "identificador": identificador, "total_servicos": len(servicos)}


def atualizar_instancia(arquivo_importado, pasta_historico=None, endereco=None):
    """Atualiza uma instância seguida; valida antes e mantém cópia histórica antes da troca atômica."""
    arquivo = Path(arquivo_importado)
    try:
        conteudo_anterior = arquivo.read_bytes()
        anterior = json.loads(conteudo_anterior.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise ValueError("Não foi possível ler a importação atual: {}".format(erro)) from erro
    if not isinstance(anterior, dict) or not isinstance(anterior.get("instancia"), dict):
        raise ValueError("Arquivo atual não contém um manifesto local de instância válido.")
    instancia_anterior = anterior["instancia"]
    identificador_anterior = instancia_anterior.get("identificador")
    endereco = endereco or instancia_anterior.get("endereco_publico")
    if not identificador_anterior or not endereco:
        raise ValueError("Arquivo atual não contém endereço e identificador da instância seguida.")
    actor, servicos = _ler_publicacao(endereco)
    if actor["preferredUsername"] != identificador_anterior:
        raise ValueError("A origem respondeu com identificador diferente da instância seguida.")
    nova_versao = _montar_importacao(actor, servicos)
    conteudo_novo = json.dumps(nova_versao, ensure_ascii=False, indent=2) + "\n"

    historico = Path(pasta_historico) if pasta_historico else arquivo.parent / "historico"
    historico.mkdir(parents=True, exist_ok=True)
    marca_tempo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    nome_base = "{}_{}.json".format(identificador_anterior, marca_tempo)
    copia = historico / nome_base
    sufixo = 1
    while copia.exists():
        copia = historico / "{}_{}_{}.json".format(identificador_anterior, marca_tempo, sufixo)
        sufixo += 1
    with copia.open("xb") as destino_historico:
        destino_historico.write(conteudo_anterior)
        destino_historico.flush()
        os.fsync(destino_historico.fileno())

    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=str(arquivo.parent),
            prefix=arquivo.name + ".", suffix=".tmp", delete=False
        ) as destino:
            temporario = Path(destino.name)
            destino.write(conteudo_novo)
            destino.flush()
            os.fsync(destino.fileno())
        os.replace(str(temporario), str(arquivo))
    except Exception:
        if temporario is not None:
            try:
                temporario.unlink()
            except OSError:
                pass
        raise
    return {
        "arquivo": str(arquivo),
        "historico": str(copia),
        "identificador": identificador_anterior,
        "total_servicos": len(servicos),
    }
