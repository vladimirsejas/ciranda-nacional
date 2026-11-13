import json
import os
import tempfile
from pathlib import Path

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from ciranda.publicar import gerar_arquivos
from ciranda.servico import CAMPOS_PERMITIDOS


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


demo = Path(RAIZ) / "ciranda" / "demonstracao" / "instancia_demo"
manifesto = json.loads((demo / "manifesto.json").read_text(encoding="utf-8"))
catalogo = json.loads((demo / "catalogo.json").read_text(encoding="utf-8"))
with tempfile.TemporaryDirectory() as pasta:
    gerados = gerar_arquivos(manifesto, catalogo, pasta)
    webfinger = json.loads(Path(gerados["webfinger"]).read_text(encoding="utf-8"))
    actor = json.loads(Path(gerados["actor"]).read_text(encoding="utf-8"))
    outbox = json.loads(Path(gerados["outbox"]).read_text(encoding="utf-8"))
    checar("os três arquivos gerados são JSON válido", bool(webfinger and actor and isinstance(outbox, dict)))
    checar("WebFinger aponta para o perfil da instância", webfinger["links"][0]["href"] == actor["id"])
    checar("perfil e lista de publicações têm estrutura esperada",
           actor["outbox"] == outbox["id"] and outbox["type"] == "OrderedCollection")
    servicos = [a["object"]["ciranda:servico"] for a in outbox["orderedItems"]]
    checar("todos os serviços do catálogo foram publicados", len(servicos) == len(catalogo))
    checar("todos os documentos usam somente campos permitidos",
           all(set(s).issubset(set(CAMPOS_PERMITIDOS)) for s in servicos))
    checar("itens fictícios mantêm a marca DEMONSTRAÇÃO",
           all("DEMONSTRAÇÃO" in s["titulo"] for s in servicos))
    proibidos = {"pessoa", "nome_pessoa", "cpf", "nascimento", "internacao", "cnes"}
    checar("nenhum campo proibido aparece nos documentos",
           all(not proibidos.intersection(s) for s in servicos))
print("Teste de publicação concluído.")
