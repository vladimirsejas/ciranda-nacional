"""MISM — um projeto só, construído sobre o MISM2 (painel, Apoio à mulher, Onde ser atendida, Hospitais de câncer).

O mapa de Rio Claro do projeto do grupo (MISM 1) entra como mais uma página do MISM2, ao lado do Apoio à mulher.

Este arquivo só monta a navegação. O código de cada projeto continua nas suas pastas, e as páginas do MISM2
são registradas como estão (a barra interna delas continua funcionando e ganhou o destino "Mapa de Rio Claro").

Rodar:  streamlit run app.py
"""
import os
import sys
from pathlib import Path

import streamlit as st

# O MISM2 foi feito para rodar com dashboard/app.py como entrada (os módulos irmãos, como lia_rosto e estilo,
# são importados direto): a pasta dashboard precisa estar no caminho de importação.
sys.path.insert(0, str(Path(__file__).resolve().parent / "MISM2" / "dashboard"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "MISM2" / "algoritimos"))
# A Ciranda mantém seus módulos novos isolados em sua própria pasta.
sys.path.insert(0, str(Path(__file__).resolve().parent))

st.set_page_config(page_title="MISM · Saúde da Mulher", page_icon="💗", layout="wide", initial_sidebar_state="collapsed")

D = "MISM2/dashboard"
apoio = st.Page(f"{D}/pages/apoio.py", title="Apoio à mulher", url_path="apoio")
rede_ciranda = st.Page("ciranda/paginas/rede_ciranda.py", title="Rede Ciranda", icon="🔗", url_path="rede_ciranda", default=True)

# O MISM2 é a tela inicial; a navegação entre as páginas é a barra do próprio MISM2 (a do Streamlit fica escondida).
pagina = st.navigation([rede_ciranda, apoio], position="hidden")
pagina.run()
