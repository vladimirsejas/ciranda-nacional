"""Página de consulta aos serviços públicos recebidos de outras instâncias."""
import html
import json
import os
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from ciranda.seguir import seguir_instancia  # noqa: E402

PASTA_IMPORTADOS = RAIZ / "ciranda" / "importados"


def carregar_importacoes(pasta=PASTA_IMPORTADOS):
    """Lê apenas os arquivos locais de instâncias seguidas."""
    pasta = Path(pasta)
    if not pasta.exists():
        return []
    resultados = []
    for arquivo in sorted(pasta.glob("*.json")):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
            if isinstance(dados, dict) and isinstance(dados.get("servicos"), list):
                resultados.append((arquivo, dados))
        except (OSError, json.JSONDecodeError):
            continue
    return resultados


st.set_page_config(page_title="Rede Ciranda", page_icon="🔗", layout="wide")
st.title("Rede Ciranda")
st.write("Veja serviços de apoio publicados por outras instâncias da Ciranda. As informações continuam sob responsabilidade de quem publicou.")

with st.form("ciranda_seguir_form"):
    endereco = st.text_input("Endereço público da outra instância", placeholder="https://exemplo.org")
    adicionar = st.form_submit_button("Seguir instância")
if adicionar:
    if not endereco.strip():
        st.error("Informe o endereço HTTPS da instância.")
    else:
        try:
            resultado = seguir_instancia(endereco.strip(), PASTA_IMPORTADOS)
            st.success("{} serviço(s) importado(s) de {}.".format(
                resultado["total_servicos"], resultado["identificador"]))
        except FileExistsError as erro:
            st.warning(str(erro))
        except (ValueError, OSError) as erro:
            st.error(str(erro))

instancias = carregar_importacoes()
if not instancias:
    st.info("Você ainda não está seguindo outra instância. Informe acima o endereço público de uma instância Ciranda.")
else:
    st.subheader("Instâncias seguidas")
    for arquivo, dados in instancias:
        instancia = dados.get("instancia", {})
        nome = instancia.get("nome") or instancia.get("identificador") or arquivo.stem
        st.markdown("### " + str(nome))
        st.caption("Endereço público: " + str(instancia.get("endereco_publico", "não informado")))
        servicos = dados.get("servicos", [])
        if not servicos:
            st.caption("Esta instância ainda não publicou serviços.")
        for registro in servicos:
            servico = registro.get("servico", {})
            origem = registro.get("origem") or instancia.get("identificador") or "instância externa"
            data = registro.get("data_conferencia_publicada") or "não informada"
            st.markdown(
                '<div style="display:inline-block;background:#eee8f7;color:#49376f;'
                'padding:6px 12px;border-radius:18px;font-weight:700;">Informado por '
                + html.escape(str(origem)) + ' · verificado em ' + html.escape(str(data))
                + '</div>', unsafe_allow_html=True)
            st.warning("Esta instância não verificou este item.")
            st.markdown("**" + str(servico.get("titulo", "Serviço sem título")) + "**")
            if servico.get("resumo"):
                st.write(servico["resumo"])
            if servico.get("para_quem"):
                st.write("**Para quem:** " + servico["para_quem"])
            if servico.get("como"):
                st.write("**Como acessar:** " + servico["como"])
            if servico.get("onde"):
                st.write("**Onde:** " + servico["onde"])
            if servico.get("contato"):
                st.write("**Contato:** " + servico["contato"])
            if servico.get("fonte"):
                st.caption("Fonte informada: " + servico["fonte"])
            if servico.get("link", "").startswith("https://"):
                st.link_button("Abrir fonte publicada", servico["link"])
            if servico.get("a_confirmar"):
                st.caption("A publicação informa que este item ainda precisa de confirmação.")
            st.divider()
