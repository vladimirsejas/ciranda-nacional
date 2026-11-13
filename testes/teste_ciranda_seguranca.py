import json
import os
import socket
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from ciranda import seguir
from ciranda.publicar import gerar_arquivos


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


def deve_falhar(funcao, tipo=ValueError):
    try:
        funcao()
    except tipo:
        return True
    return False


def preparar_publicacao(pasta, titulo="DEMONSTRAÇÃO — Serviço original"):
    demo = RAIZ / "ciranda" / "demonstracao" / "instancia_demo"
    manifesto = json.loads((demo / "manifesto.json").read_text(encoding="utf-8"))
    catalogo = [{
        "id": "demo-item",
        "titulo": titulo,
        "resumo": "Resumo de demonstração",
        "para_quem": "Público de demonstração",
        "como": "Instrução de demonstração",
        "contato": "Contato fictício",
        "fonte": "Fonte fictícia",
        "link": "https://links.exemplo.invalid/servico",
        "onde": "Local fictício",
        "conferido": "2026-11-13",
        "confirmar": None,
    }]
    gerar_arquivos(manifesto, catalogo, pasta)
    return manifesto, catalogo


# Endereços locais e IPs numéricos não podem ser consultados.
checar("localhost é recusado", deve_falhar(
    lambda: seguir._resolver_endereco_publico("https://localhost")))
checar("IP numérico público também é recusado", deve_falhar(
    lambda: seguir._resolver_endereco_publico("https://8.8.8.8")))

getaddrinfo_original = socket.getaddrinfo
try:
    socket.getaddrinfo = lambda *args, **kwargs: [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.8", 443))
    ]
    checar("nome DNS que resolve para IP privado é recusado", deve_falhar(
        lambda: seguir._resolver_endereco_publico("https://servico.exemplo.org")))
finally:
    socket.getaddrinfo = getaddrinfo_original


# Resposta maior que 2 MB é interrompida mesmo sem Content-Length.
class RespostaGrande:
    status = 200

    def getheader(self, nome):
        return None

    def read(self, limite):
        return b"x" * limite


class ConexaoFalsa:
    def __init__(self, *args, **kwargs):
        pass

    def request(self, *args, **kwargs):
        pass

    def getresponse(self):
        return RespostaGrande()

    def close(self):
        pass


getaddrinfo_original = socket.getaddrinfo
https_original = seguir.http.client.HTTPSConnection
try:
    socket.getaddrinfo = lambda *args, **kwargs: [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
    ]
    seguir.http.client.HTTPSConnection = ConexaoFalsa
    checar("resposta acima de 2 MB é recusada", deve_falhar(
        lambda: seguir._baixar_corpo_https("https://publico.exemplo.org/actor.json")))
finally:
    socket.getaddrinfo = getaddrinfo_original
    seguir.http.client.HTTPSConnection = https_original


with tempfile.TemporaryDirectory() as temporario:
    raiz = Path(temporario)
    publicacao = raiz / "publicacao"
    importados = raiz / "importados"
    manifesto, catalogo = preparar_publicacao(publicacao)
    primeiro = seguir.seguir_instancia(publicacao, importados)
    arquivo = Path(primeiro["arquivo"])
    conteudo_anterior = arquivo.read_text(encoding="utf-8")

    # Atualização bem-sucedida preserva uma cópia histórica e troca os serviços.
    preparar_publicacao(publicacao, "DEMONSTRAÇÃO — Serviço atualizado")
    resultado = seguir.atualizar_instancia(arquivo)
    atualizado = json.loads(arquivo.read_text(encoding="utf-8"))
    historico = Path(resultado["historico"])
    anterior = json.loads(historico.read_text(encoding="utf-8"))
    checar("atualização bem-sucedida substitui o catálogo importado",
           atualizado["servicos"][0]["servico"]["titulo"] == "DEMONSTRAÇÃO — Serviço atualizado")
    checar("atualização guarda versão anterior no histórico",
           historico.exists()
           and anterior["servicos"][0]["servico"]["titulo"] == "DEMONSTRAÇÃO — Serviço original")

    # Uma publicação inválida deve falhar antes de qualquer substituição.
    conteudo_antes_falha = arquivo.read_bytes()
    (publicacao / "outbox.json").write_text("{ JSON inválido", encoding="utf-8")
    falhou = deve_falhar(lambda: seguir.atualizar_instancia(arquivo))
    checar("atualização com arquivo inválido falha", falhou)
    checar("falha de atualização preserva integralmente a versão atual",
           arquivo.read_bytes() == conteudo_antes_falha)


# Limite de quantidade de serviços e tamanho individual de texto.
with tempfile.TemporaryDirectory() as temporario:
    pasta = Path(temporario)
    manifesto, catalogo = preparar_publicacao(pasta)
    actor = json.loads((pasta / "actor.json").read_text(encoding="utf-8"))
    outbox = json.loads((pasta / "outbox.json").read_text(encoding="utf-8"))
    outbox["orderedItems"] = outbox["orderedItems"] * 501
    (pasta / "outbox.json").write_text(json.dumps(outbox), encoding="utf-8")
    checar("mais de 500 serviços são recusados", deve_falhar(
        lambda: seguir._ler_publicacao(pasta)))
    gerar_arquivos(manifesto, catalogo, pasta)
    outbox = json.loads((pasta / "outbox.json").read_text(encoding="utf-8"))
    outbox["orderedItems"][0]["object"]["ciranda:servico"]["resumo"] = "x" * (seguir.MAX_CAMPO_TEXTO + 1)
    (pasta / "outbox.json").write_text(json.dumps(outbox), encoding="utf-8")
    checar("campo de texto acima do limite é recusado", deve_falhar(
        lambda: seguir._ler_publicacao(pasta)))

print("Testes de segurança e atualização concluídos.")
