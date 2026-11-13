"""Manifesto público e validação de uma instância Ciranda."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

IDENTIFICADOR_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CAMPOS_COMUNS = ("nome", "tipo", "endereco_publico", "contato_publico", "identificador")


def validar_manifesto(manifesto):
    """Retorna uma lista de erros legíveis; lista vazia significa manifesto válido."""
    erros = []
    if not isinstance(manifesto, dict):
        return ["O manifesto deve ser um objeto JSON."]
    for campo in CAMPOS_COMUNS:
        valor = manifesto.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            erros.append("O campo '{}' é obrigatório e deve conter texto.".format(campo))
    tipo = manifesto.get("tipo")
    if tipo not in ("cidade", "organizacao"):
        erros.append("O campo 'tipo' deve ser 'cidade' ou 'organizacao'.")
    if tipo == "cidade":
        if not isinstance(manifesto.get("municipio"), str) or not manifesto["municipio"].strip():
            erros.append("Para uma instância do tipo 'cidade', informe 'municipio'.")
    if tipo == "organizacao":
        if not isinstance(manifesto.get("organizacao"), str) or not manifesto["organizacao"].strip():
            erros.append("Para uma instância do tipo 'organizacao', informe 'organizacao'.")
    identificador = manifesto.get("identificador")
    if isinstance(identificador, str) and identificador and not IDENTIFICADOR_RE.fullmatch(identificador):
        erros.append("O identificador deve usar apenas letras minúsculas sem acento, números e hífens, sem hífen no início ou no fim.")
    endereco = manifesto.get("endereco_publico")
    if isinstance(endereco, str) and endereco.strip():
        partes = urlparse(endereco.strip())
        if partes.scheme != "https" or not partes.netloc or partes.username or partes.password:
            erros.append("O endereço público deve ser uma URL HTTPS válida, sem usuário ou senha.")
    return erros


def carregar_manifesto(caminho):
    """Lê um manifesto JSON e devolve o objeto validado."""
    caminho = Path(caminho)
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            manifesto = json.load(arquivo)
    except FileNotFoundError as erro:
        raise ValueError("Manifesto não encontrado: {}".format(caminho)) from erro
    except json.JSONDecodeError as erro:
        raise ValueError("O manifesto não contém JSON válido: {}".format(erro)) from erro
    erros = validar_manifesto(manifesto)
    if erros:
        raise ValueError("Manifesto inválido:\n- " + "\n- ".join(erros))
    return manifesto
