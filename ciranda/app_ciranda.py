"""Ponto de entrada independente do protótipo Ciranda."""
import json
import os
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from ciranda.seguir import seguir_instancia

PASTA_IMPORTADOS = Path(os.environ.get(
    "CIRANDA_IMPORTADOS_DIR", str(RAIZ / "ciranda" / "importados")
))
DEMO = RAIZ / "ciranda" / "demonstracao" / "instancia_demo"


def importar_demo_se_necessario(pasta_importados=PASTA_IMPORTADOS):
    """Importa uma única vez a instância fictícia, sem substituir arquivo existente."""
    pasta_importados = Path(pasta_importados)
    manifesto = json.loads((DEMO / "manifesto.json").read_text(encoding="utf-8"))
    identificador = manifesto["identificador"]
    arquivo_existente = pasta_importados / (identificador + ".json")
    if arquivo_existente.exists():
        return False
    seguir_instancia(DEMO, pasta_importados)
    return True


st.set_page_config(page_title="Ciranda", page_icon="🔗", layout="wide")
st.info("Protótipo de pesquisa. Os serviços exibidos são fictícios, de demonstração.")

try:
    importar_demo_se_necessario()
except (OSError, ValueError, json.JSONDecodeError) as erro:
    st.error("Não foi possível carregar a demonstração: {}".format(erro))

pagina = st.navigation([
    st.Page(str(RAIZ / "ciranda" / "paginas" / "rede_ciranda.py"),
            title="Rede Ciranda", icon="🔗", url_path="rede_ciranda", default=True)
], position="hidden")
pagina.run()
