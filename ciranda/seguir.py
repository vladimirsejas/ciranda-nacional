"""Leitura e importação isolada de catálogos publicados por outra instância."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from ciranda.servico import CAMPOS_PERMITIDOS

IDENTIFICADOR_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _ler_json_local_ou_url(origem, nome):
    caminho = Path(str(origem))
    if caminho.is_dir():
        arquivo = caminho / nome
        try:
            return json.loads(arquivo.read_text(encoding="utf-8"))
        except FileNotFoundError as erro:
            raise ValueError("Arquivo obrigatório não encontrado: {}".format(arquivo)) from erro
        except json.JSONDecodeError as erro:
            raise ValueError("JSON inválido em {}: {}".format(arquivo, erro)) from erro
    base = str(origem).rstrip("/")
    partes = urlparse(base)
    if partes.scheme != "https" or not partes.netloc:
        raise ValueError("Informe uma pasta local existente ou um endereço HTTPS de outra instância.")
    url = base + "/" + nome
    requisicao = Request(url, headers={"Accept": "application/activity+json, application/json"})
    try:
        with urlopen(requisicao, timeout=15) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except Exception as erro:
        raise ValueError("Não foi possível ler {}: {}".format(url, erro)) from erro


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
    identificador = actor.get("preferredUsername")
    if not isinstance(identificador, str) or not IDENTIFICADOR_RE.fullmatch(identificador):
        raise ValueError("Perfil inválido: identificador da instância ausente ou inválido.")
    if not isinstance(actor.get("id"), str) or not actor["id"].startswith("https://"):
        raise ValueError("Perfil inválido: endereço público do perfil ausente ou inválido.")
    if not isinstance(outbox, dict) or outbox.get("type") != "OrderedCollection":
        raise ValueError("Lista de publicações inválida: esperado OrderedCollection.")
    atividades = outbox.get("orderedItems")
    if not isinstance(atividades, list):
        raise ValueError("Lista de publicações inválida: 'orderedItems' deve ser uma lista.")
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
        if documento.get("origem_instancia") != identificador:
            raise ValueError("Publicação {} informa origem diferente da instância publicadora.".format(indice))
        if not documento.get("id") or not documento.get("data_conferencia"):
            raise ValueError("Publicação {} não informa id ou data de conferência.".format(indice))
        servicos.append(documento)
    return actor, servicos


def seguir_instancia(endereco, pasta_importados="ciranda/importados"):
    """Importa serviços em arquivo separado; nunca altera o catálogo local nem sobrescreve importação."""
    actor, servicos = _ler_publicacao(endereco)
    identificador = actor["preferredUsername"]
    destino = Path(pasta_importados)
    destino.mkdir(parents=True, exist_ok=True)
    arquivo = destino / (identificador + ".json")
    if arquivo.exists():
        raise FileExistsError("Esta instância já possui arquivo de importação: {}".format(arquivo))
    importado_em = datetime.now(timezone.utc).isoformat()
    dados = {
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
    arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"arquivo": str(arquivo), "identificador": identificador, "total_servicos": len(servicos)}
