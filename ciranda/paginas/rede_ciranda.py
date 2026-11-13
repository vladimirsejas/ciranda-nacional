"""Página de consulta aos serviços públicos recebidos de outras instâncias."""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from ciranda.seguir import atualizar_instancia, seguir_instancia  # noqa: E402

PASTA_IMPORTADOS = Path(os.environ.get(
    "CIRANDA_IMPORTADOS_DIR", str(RAIZ / "ciranda" / "importados")
))


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


def dominio_link(url):
    """Retorna apenas o domínio de um link HTTPS válido."""
    if not isinstance(url, str):
        return ""
    try:
        partes = urlparse(url)
        porta = partes.port
    except ValueError:
        return ""
    if partes.scheme != "https" or not partes.hostname or partes.username or partes.password:
        return ""
    return partes.hostname


st.set_page_config(page_title="Rede Ciranda", page_icon="🔗", layout="wide")
st.title("Rede Ciranda")
st.text("Veja serviços de apoio publicados por outras instâncias da Ciranda. As informações continuam sob responsabilidade de quem publicou.")

with st.form("ciranda_seguir_form"):
    endereco = st.text_input("Endereço público da outra instância", placeholder="https://exemplo.org")
    adicionar = st.form_submit_button("Seguir instância")
if adicionar:
    if not endereco.strip():
        st.error("Informe o endereço HTTPS da instância.")
    else:
        try:
            resultado = seguir_instancia(endereco.strip(), PASTA_IMPORTADOS)
            st.text("{} serviço(s) importado(s) de {}.".format(
                resultado["total_servicos"], resultado["identificador"]))
        except FileExistsError as erro:
            st.text(str(erro))
        except (ValueError, OSError) as erro:
            st.text(str(erro))

instancias = carregar_importacoes()
if not instancias:
    st.info("Você ainda não está seguindo outra instância. Informe acima o endereço público de uma instância Ciranda.")
else:
    st.subheader("Instâncias seguidas")
    for arquivo, dados in instancias:
        instancia = dados.get("instancia", {})
        nome = instancia.get("nome") or instancia.get("identificador") or arquivo.stem
        identificador = instancia.get("identificador") or arquivo.stem
        st.text("Instância: " + str(nome))
        st.text("Endereço público: " + str(instancia.get("endereco_publico", "não informado")))
        if st.button("Atualizar", key="atualizar_" + str(identificador)):
            try:
                resultado = atualizar_instancia(arquivo)
                st.text("{} serviço(s) atualizados.".format(resultado["total_servicos"]))
                st.rerun()
            except (ValueError, OSError) as erro:
                st.text("Atualização não realizada. A versão anterior foi preservada. {}".format(erro))
        servicos = dados.get("servicos", [])
        if not servicos:
            st.text("Esta instância ainda não publicou serviços.")
        for registro in servicos:
            servico = registro.get("servico", {})
            origem = "{} ({})".format(nome, registro.get("origem") or identificador)
            data = registro.get("data_conferencia_publicada") or "não informada"
            st.text("Informado por {} · verificado em {}".format(origem, data))
            st.warning("Esta instância não verificou este item.")
            st.text(servico.get("titulo", "Serviço sem título"))
            if servico.get("resumo"):
                st.text(servico["resumo"])
            if servico.get("para_quem"):
                st.text("Para quem: " + servico["para_quem"])
            if servico.get("como"):
                st.text("Como acessar: " + servico["como"])
            if servico.get("onde"):
                st.text("Onde: " + servico["onde"])
            if servico.get("contato"):
                st.text("Contato: " + servico["contato"])
            if servico.get("fonte"):
                st.text("Fonte informada: " + servico["fonte"])
            link = servico.get("link", "")
            dominio = dominio_link(link)
            if dominio:
                st.text("Domínio do link: " + dominio)
                st.text("Link informado por outra instância; confira antes de usar")
                st.link_button("Abrir fonte informada", link)
            if servico.get("a_confirmar"):
                st.text("A publicação informa que este item ainda precisa de confirmação.")
            st.divider()
