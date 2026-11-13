import os
import sys
import tempfile
from pathlib import Path

from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


with tempfile.TemporaryDirectory() as pasta:
    anterior = os.environ.get("CIRANDA_IMPORTADOS_DIR")
    os.environ["CIRANDA_IMPORTADOS_DIR"] = pasta
    try:
        at = AppTest.from_file(str(RAIZ / "ciranda" / "app_ciranda.py"), default_timeout=60)
        at.run()
        checar("ponto de entrada Ciranda abre sem exceções", len(at.exception) == 0)
        checar("faixa de protótipo aparece no topo",
               any("Protótipo de pesquisa. Os serviços exibidos são fictícios, de demonstração."
                   in str(item.value) for item in at.info))
        demo = Path(pasta) / "instancia-a-demo.json"
        checar("primeira abertura importa automaticamente a demonstração", demo.exists())
        texto = demo.read_text(encoding="utf-8")
        checar("a demonstração importada contém os serviços fictícios",
               "DEMONSTRAÇÃO" in texto and "demo-acolhimento" in texto)
        original = texto
        at.run()
        checar("reabrir o ponto de entrada não sobrescreve importação existente",
               demo.read_text(encoding="utf-8") == original)
    finally:
        if anterior is None:
            os.environ.pop("CIRANDA_IMPORTADOS_DIR", None)
        else:
            os.environ["CIRANDA_IMPORTADOS_DIR"] = anterior
print("Teste do ponto de entrada Ciranda concluído.")
