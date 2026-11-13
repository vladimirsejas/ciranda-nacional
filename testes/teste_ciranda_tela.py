import json
import os
import sys
import tempfile
from pathlib import Path

from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from ciranda.publicar import gerar_arquivos
from ciranda.seguir import seguir_instancia


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


at = AppTest.from_file(str(RAIZ / "ciranda" / "paginas" / "rede_ciranda.py"), default_timeout=60)
with tempfile.TemporaryDirectory() as pasta:
    importados = Path(pasta)
    demo = RAIZ / "ciranda" / "demonstracao" / "instancia_demo"
    manifesto = json.loads((demo / "manifesto.json").read_text(encoding="utf-8"))
    catalogo = [{
        "id": "teste-texto",
        "titulo": "Título **não formatar** <b>nem HTML</b>",
        "resumo": "Resumo com **Markdown** e <script>alert('x')</script>",
        "para_quem": "Público de teste",
        "como": "Instrução simples",
        "contato": "Contato fictício",
        "fonte": "Fonte fictícia",
        "link": "https://links.exemplo.invalid/item",
        "onde": "Local fictício",
        "conferido": "2026-11-13",
        "confirmar": None,
    }]
    publicacao = importados / "publicacao"
    gerar_arquivos(manifesto, catalogo, publicacao)
    seguir_instancia(publicacao, importados)
    anterior = os.environ.get("CIRANDA_IMPORTADOS_DIR")
    os.environ["CIRANDA_IMPORTADOS_DIR"] = str(importados)
    try:
        at.run()
    finally:
        if anterior is None:
            os.environ.pop("CIRANDA_IMPORTADOS_DIR", None)
        else:
            os.environ["CIRANDA_IMPORTADOS_DIR"] = anterior

    textos = [str(item.value) for item in at.text]
    checar("página Rede Ciranda abre sem exceções", len(at.exception) == 0)
    checar("texto remoto com Markdown e HTML aparece literalmente",
           any("Título **não formatar** <b>nem HTML</b>" in valor for valor in textos)
           and any("<script>alert('x')</script>" in valor for valor in textos))
    checar("página mostra o domínio e o aviso de cautela do link",
           any("Domínio do link: links.exemplo.invalid" in valor for valor in textos)
           and any("Link informado por outra instância; confira antes de usar" in valor for valor in textos))
    checar("página oferece atualização por instância",
           any(botao.label == "Atualizar" for botao in at.button))
    checar("página não cria elementos Markdown para o conteúdo remoto", len(at.markdown) == 0)
print("Teste de tela da Rede Ciranda concluído.")
