"""Verificação de conformidade de uma publicação Ciranda."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from ciranda.seguir import (
    CAMPOS_PERMITIDOS,
    IDENTIFICADOR_RE,
    MAX_CAMPO_TEXTO,
    MAX_RESPOSTA_BYTES,
    MAX_SERVICOS,
    _baixar_corpo_https,
    _ler_json_local_ou_url,
)

CAMPOS_OBRIGATORIOS_IMPORTACAO = ("id", "data_conferencia", "origem_instancia")


def _ler_descoberta(origem):
    if Path(str(origem)).is_dir():
        caminho = Path(origem) / ".well-known" / "webfinger"
        conteudo = caminho.read_bytes()
        if len(conteudo) > MAX_RESPOSTA_BYTES:
            raise ValueError("Arquivo de descoberta excede 2 MB.")
        return json.loads(conteudo.decode("utf-8"))
    base = str(origem).rstrip("/")
    return json.loads(_baixar_corpo_https(base + "/.well-known/webfinger").decode("utf-8"))


def _data_reconhecida(valor):
    if not isinstance(valor, str) or not valor.strip():
        return False
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            date.strptime(valor.strip(), formato)
            return True
        except (ValueError, AttributeError):
            pass
    # date.strptime não existe em algumas versões suportadas; tenta datetime.
    from datetime import datetime
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            datetime.strptime(valor.strip(), formato)
            return True
        except ValueError:
            pass
    return False


def _cpf_valido(numero):
    digitos = re.sub(r"\D", "", numero)
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
    primeiro = (soma * 10) % 11
    primeiro = 0 if primeiro == 10 else primeiro
    if primeiro != int(digitos[9]):
        return False
    soma = sum(int(digitos[i]) * (11 - i) for i in range(10))
    segundo = (soma * 10) % 11
    segundo = 0 if segundo == 10 else segundo
    return segundo == int(digitos[10])


def _textos(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for chave, item in valor.items():
            if isinstance(chave, str):
                yield chave
            yield from _textos(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from _textos(item)


def _achados_privacidade(valor):
    achados = []
    vistos = set()
    for texto in _textos(valor):
        for trecho in re.findall(r"(?<!\d)(?:\d[ .-]?){10}\d(?!\d)", texto):
            numero = re.sub(r"\D", "", trecho)
            if _cpf_valido(numero) and ("CPF", numero) not in vistos:
                vistos.add(("CPF", numero))
                achados.append("CPF com dígitos verificadores válidos detectado por heurística.")
        for numero in re.findall(r"(?<!\d)\d{15}(?!\d)", texto):
            if ("CNS", numero) not in vistos:
                vistos.add(("CNS", numero))
                achados.append("Sequência de 15 dígitos compatível com Cartão SUS detectada por heurística.")
    return achados


def verificar_instancia(endereco_ou_pasta):
    """Retorna relatório estruturado; não altera a instância verificada."""
    origem = str(endereco_ou_pasta)
    verificacoes = []

    def registrar(nome, resultado, explicacao):
        verificacoes.append({"nome": nome, "resultado": resultado, "explicacao": explicacao})

    try:
        descoberta = _ler_descoberta(origem)
        if not isinstance(descoberta, dict):
            raise ValueError("O documento de descoberta não é um objeto JSON.")
        links = descoberta.get("links")
        link_perfil = next((l for l in links if isinstance(l, dict) and l.get("rel") == "self"), None) if isinstance(links, list) else None
        if not link_perfil or not isinstance(link_perfil.get("href"), str):
            registrar("descoberta aponta para perfil", "ERRO", "O arquivo existe, mas não contém link self com href.")
            return {"origem": origem, "verificacoes": verificacoes}
        href = link_perfil["href"]
        registrar("arquivo de descoberta existe e aponta para perfil", "OK",
                  "O documento .well-known/webfinger foi lido e contém link self.")
    except (OSError, ValueError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as erro:
        registrar("arquivo de descoberta existe e aponta para perfil", "ERRO", str(erro))
        return {"origem": origem, "verificacoes": verificacoes}

    try:
        actor = _ler_json_local_ou_url(origem, "actor.json")
        if not isinstance(actor, dict):
            raise ValueError("O perfil não é um objeto JSON.")
        tipo_ok = actor.get("type") == "Organization"
        registrar("perfil do tipo Organization", "OK" if tipo_ok else "ERRO",
                  "Perfil é Organization." if tipo_ok else "Tipo de perfil diferente de Organization.")
        identificador = actor.get("preferredUsername")
        id_ok = isinstance(identificador, str) and bool(IDENTIFICADOR_RE.fullmatch(identificador))
        registrar("identificador válido", "OK" if id_ok else "ERRO",
                  "Identificador segue letras minúsculas, números e hífens." if id_ok else "Identificador ausente ou fora do formato permitido.")
        endereco_perfil = actor.get("id")
        partes = urlparse(endereco_perfil) if isinstance(endereco_perfil, str) else None
        https_ok = bool(partes and partes.scheme == "https" and partes.hostname
                        and not partes.username and not partes.password
                        and not partes.query and not partes.fragment
                        and partes.path.endswith("/actor.json"))
        registrar("endereço HTTPS do perfil", "OK" if https_ok else "ERRO",
                  "O id do perfil é uma URL HTTPS terminada em /actor.json." if https_ok else "O id do perfil não é uma URL HTTPS válida terminada em /actor.json.")
        if Path(origem).is_dir():
            perfil_corresponde = https_ok and href == endereco_perfil
        else:
            perfil_corresponde = https_ok and urlparse(href).hostname == urlparse(origem).hostname and href == endereco_perfil
        registrar("descoberta corresponde ao perfil", "OK" if perfil_corresponde else "ERRO",
                  "O href da descoberta corresponde ao id do perfil." if perfil_corresponde else "O href da descoberta não corresponde ao perfil publicado.")
    except (OSError, ValueError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as erro:
        registrar("leitura do perfil", "ERRO", str(erro))
        return {"origem": origem, "verificacoes": verificacoes}

    try:
        outbox = _ler_json_local_ou_url(origem, "outbox.json")
        colecao_ok = isinstance(outbox, dict) and outbox.get("type") == "OrderedCollection"
        registrar("lista de publicações OrderedCollection", "OK" if colecao_ok else "ERRO",
                  "A lista usa OrderedCollection." if colecao_ok else "A lista não usa OrderedCollection.")
        atividades = outbox.get("orderedItems") if isinstance(outbox, dict) else None
        lista_ok = isinstance(atividades, list)
        registrar("orderedItems é uma lista", "OK" if lista_ok else "ERRO",
                  "orderedItems é uma lista." if lista_ok else "orderedItems ausente ou não é lista.")
        if not lista_ok:
            atividades = []
        qtd_ok = len(atividades) <= MAX_SERVICOS
        registrar("limite de quantidade", "OK" if qtd_ok else "ERRO",
                  "{} publicação(ões); máximo permitido: {}.".format(len(atividades), MAX_SERVICOS))
    except (OSError, ValueError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as erro:
        registrar("leitura da lista de publicações", "ERRO", str(erro))
        return {"origem": origem, "verificacoes": verificacoes}

    atividade_erros = []
    documento_erros = []
    data_avisos = []
    docs = []
    for indice, atividade in enumerate(atividades, 1):
        if not isinstance(atividade, dict) or atividade.get("type") != "Create":
            atividade_erros.append("Publicação {} não é Create.".format(indice))
            continue
        if atividade.get("actor") != actor.get("id"):
            atividade_erros.append("Publicação {} pertence a outro perfil.".format(indice))
        objeto = atividade.get("object")
        documento = objeto.get("ciranda:servico") if isinstance(objeto, dict) else None
        if not isinstance(documento, dict):
            documento_erros.append("Publicação {} não contém documento de serviço.".format(indice))
            continue
        docs.append(documento)
        extras = set(documento) - set(CAMPOS_PERMITIDOS)
        if extras:
            documento_erros.append("Publicação {} contém campos proibidos: {}.".format(indice, ", ".join(sorted(extras))))
        faltantes = [c for c in CAMPOS_OBRIGATORIOS_IMPORTACAO if not isinstance(documento.get(c), str) or not documento.get(c).strip()]
        if faltantes:
            documento_erros.append("Publicação {} sem obrigatórios: {}.".format(indice, ", ".join(faltantes)))
        if documento.get("origem_instancia") != identificador:
            documento_erros.append("Publicação {} informa origem diferente do perfil.".format(indice))
        for campo, valor in documento.items():
            if campo == "a_confirmar":
                if not isinstance(valor, bool):
                    documento_erros.append("Publicação {} tem a_confirmar fora do tipo booleano.".format(indice))
            elif not isinstance(valor, str):
                documento_erros.append("Publicação {} tem campo {} que não é texto.".format(indice, campo))
            elif len(valor) > MAX_CAMPO_TEXTO:
                documento_erros.append("Publicação {} tem campo {} acima de {} caracteres.".format(indice, campo, MAX_CAMPO_TEXTO))
        data = documento.get("data_conferencia")
        if isinstance(data, str) and data.strip() and not _data_reconhecida(data):
            data_avisos.append("Publicação {} usa data não reconhecida: {!r}.".format(indice, data))

    registrar("cada atividade pertence ao perfil", "OK" if not atividade_erros else "ERRO",
              "Todas as atividades são Create e usam o id do perfil como actor." if not atividade_erros else " ".join(atividade_erros))
    registrar("documentos usam campos permitidos e obrigatórios", "OK" if not documento_erros else "ERRO",
              "Documentos respeitam a lista permitida e os obrigatórios da importação." if not documento_erros else " ".join(documento_erros))
    registrar("formato da data de conferência", "AVISO" if data_avisos else "OK",
              " ".join(data_avisos) if data_avisos else "Datas preenchidas seguem DD/MM/AAAA ou AAAA-MM-DD; o código de importação não impõe formato.")

    privacidade = _achados_privacidade({"perfil": actor, "publicacoes": docs})
    registrar("checagem heurística de privacidade", "AVISO" if privacidade else "OK",
              " ".join(privacidade) if privacidade else "Nenhum CPF válido ou sequência de 15 dígitos foi detectado pela heurística; isso não garante ausência de dados pessoais.")

    # A leitura comum aplica o limite de 2 MiB a cada arquivo; a leitura dos textos
    # acima aplica o limite por campo. Aqui a verificação registra os limites em conjunto.
    registrar("limites de tamanho", "OK",
              "Arquivos/respostas limitados a 2 MiB e textos a {} caracteres, conforme leitura compartilhada com seguir.py.".format(MAX_CAMPO_TEXTO))
    return {"origem": origem, "verificacoes": verificacoes}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verifica a conformidade de uma instância Ciranda.")
    parser.add_argument("endereco_ou_pasta", help="URL HTTPS ou pasta com webfinger, actor.json e outbox.json")
    args = parser.parse_args(argv)
    try:
        relatorio = verificar_instancia(args.endereco_ou_pasta)
    except Exception as erro:
        print("ERRO: não foi possível concluir a verificação: {}".format(erro))
        return 1
    print("Relatório de conformidade — {}".format(relatorio["origem"]))
    for item in relatorio["verificacoes"]:
        print("[{}] {} — {}".format(item["resultado"], item["nome"], item["explicacao"]))
    return 1 if any(v["resultado"] == "ERRO" for v in relatorio["verificacoes"]) else 0


if __name__ == "__main__":
    sys.exit(main())
