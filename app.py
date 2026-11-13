"""Ciranda — plataforma federada de catálogos de serviços de apoio às mulheres.

Este é o ÚNICO ponto de entrada do site. Páginas: Rede Ciranda (inicial) e Apoio à mulher (com a Lia e a busca).
Só catálogo de serviços é federado: nenhum dado de pessoa. Não exige dados locais, segredos nem rede
(a única chamada externa da federação mora em ciranda/seguir.py, acionada pelo botão da página Rede Ciranda).

Rodar:  streamlit run app.py
"""
import json
import os
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent
# Os módulos do Apoio importam os irmãos direto (lia, estilo, apoio_busca...): as duas pastas precisam estar no caminho.
sys.path.insert(0, str(RAIZ / "MISM2" / "dashboard"))
sys.path.insert(0, str(RAIZ / "MISM2" / "algoritimos"))
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from ciranda.seguir import seguir_instancia  # noqa: E402

PASTA_IMPORTADOS = Path(os.environ.get("CIRANDA_IMPORTADOS_DIR", str(RAIZ / "ciranda" / "importados")))
DEMO = RAIZ / "ciranda" / "demonstracao" / "instancia_demo"


def importar_demo_se_necessario(pasta_importados=PASTA_IMPORTADOS):
    """Importa uma única vez a instância fictícia, sem substituir arquivo existente."""
    pasta_importados = Path(pasta_importados)
    manifesto = json.loads((DEMO / "manifesto.json").read_text(encoding="utf-8"))
    arquivo_existente = pasta_importados / (manifesto["identificador"] + ".json")
    if arquivo_existente.exists():
        return False
    seguir_instancia(DEMO, pasta_importados)
    return True


st.set_page_config(page_title="Ciranda", page_icon="🔗", layout="wide", initial_sidebar_state="collapsed")
st.title("Ciranda")
st.info("Protótipo de pesquisa. Os serviços exibidos na Rede Ciranda são fictícios, de demonstração.")

try:
    importar_demo_se_necessario()
except (OSError, ValueError, json.JSONDecodeError) as erro:
    st.error("Não foi possível carregar a demonstração: {}".format(erro))

rede_ciranda = st.Page("ciranda/paginas/rede_ciranda.py", title="Rede Ciranda", icon="🔗", url_path="rede_ciranda", default=True)
apoio = st.Page("MISM2/dashboard/pages/apoio.py", title="Apoio à mulher", icon="🩷", url_path="apoio")

# Navegação própria das páginas (a do Streamlit fica escondida): a Rede Ciranda tem o botão do Apoio e o Apoio tem o "Início".
pagina = st.navigation([rede_ciranda, apoio], position="hidden")
pagina.run()
