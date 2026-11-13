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
        at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=90)
        at.run()
        checar("app.py abre a página inicial (Rede Ciranda) sem exceções", len(at.exception) == 0)
        checar("título visível 'Ciranda'", any(str(t.value) == "Ciranda" for t in at.title))
        checar("a página inicial é a Rede Ciranda", any(str(h.value) == "Rede Ciranda" for h in at.header))
        checar("faixa de protótipo aparece no topo",
               any("Protótipo de pesquisa. Os serviços exibidos na Rede Ciranda são fictícios, de demonstração."
                   in str(item.value) for item in at.info))
        demo = Path(pasta) / "instancia-a-demo.json"
        codigo = (RAIZ / "app.py").read_text(encoding="utf-8").lower()
        checar("app.py não contém Gemini, chaves, Hugging Face, Parquet nem banco",
               not any(termo in codigo for termo in (
                   "gemini", "api_key", "token", "huggingface", "parquet", "sqlite", "banco", "tempfile", "garantir_dados"
               )))
        checar("app.py é o único ponto de entrada (ciranda/app_ciranda.py não existe mais)",
               not (RAIZ / "ciranda" / "app_ciranda.py").exists())
        checar("primeira abertura importa automaticamente a demonstração", demo.exists())
        texto = demo.read_text(encoding="utf-8")
        checar("a demonstração importada contém os serviços fictícios",
               "DEMONSTRAÇÃO" in texto and "demo-acolhimento" in texto)
        original = texto
        at.run()
        checar("reabrir o ponto de entrada não sobrescreve importação existente",
               demo.read_text(encoding="utf-8") == original)
        ap = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=120)
        ap.run()
        ap.switch_page("MISM2/dashboard/pages/apoio.py")
        ap.run()
        checar("app.py abre a página Apoio à mulher sem exceções", len(ap.exception) == 0)
        textos = " ".join(str(m.value) for m in ap.markdown)
        checar("o Apoio aparece com a marca Ciranda e a Lia", "Ciranda · Apoio à mulher" in textos and "Lia" in textos)
    finally:
        if anterior is None:
            os.environ.pop("CIRANDA_IMPORTADOS_DIR", None)
        else:
            os.environ["CIRANDA_IMPORTADOS_DIR"] = anterior
print("Teste do ponto de entrada Ciranda concluído.")
