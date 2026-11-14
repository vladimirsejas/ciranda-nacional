"""Conversão estrita de ITENS do catálogo para documentos públicos federáveis."""
import json

CAMPOS_PERMITIDOS = (
    "id", "titulo", "resumo", "para_quem", "como", "contato",
    "fonte", "link", "onde", "data_conferencia", "a_confirmar",
    "origem_instancia",
)
MAPEAMENTO = {
    "id": "id",
    "titulo": "titulo",
    "resumo": "resumo",
    "para_quem": "para_quem",
    "como": "como",
    "contato": "contato",
    "fonte": "fonte",
    "link": "link",
    "onde": "onde",
    "data_conferencia": "conferido",
}


def criar_documento_servico(item, identificador_origem):
    """Cria documento com lista fechada de campos; campos adicionais são descartados."""
    if not isinstance(item, dict):
        raise ValueError("O item do catálogo deve ser um objeto.")
    if not isinstance(identificador_origem, str) or not identificador_origem.strip():
        raise ValueError("Informe o identificador da instância de origem.")
    documento = {}
    for destino, origem in MAPEAMENTO.items():
        valor = item.get(origem)
        documento[destino] = valor if isinstance(valor, str) else ""
    documento["a_confirmar"] = bool(
        isinstance(item.get("confirmar"), str) and item["confirmar"].strip()
    )
    documento["origem_instancia"] = identificador_origem
    # A verificação explícita impede que futuras alterações ampliem a superfície de dados.
    return {campo: documento[campo] for campo in CAMPOS_PERMITIDOS}


def converter_catalogo(itens, identificador_origem):
    """Converte uma sequência de itens sem transportar campos fora da lista permitida."""
    return [criar_documento_servico(item, identificador_origem) for item in itens]


def serializar_documento(documento):
    """Serializa um documento de serviço como JSON UTF-8 legível."""
    if not isinstance(documento, dict) or set(documento) - set(CAMPOS_PERMITIDOS):
        raise ValueError("Documento contém campos não permitidos.")
    return json.dumps(documento, ensure_ascii=False, indent=2)
