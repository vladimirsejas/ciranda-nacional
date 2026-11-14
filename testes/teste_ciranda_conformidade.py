import json
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from ciranda.conformidade import verificar_instancia, _achados_privacidade
from ciranda.servico import CAMPOS_PERMITIDOS, converter_catalogo


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


PASTA_CASOS = RAIZ / "ciranda" / "demonstracao" / "conformidade"
CASOS = {
    "instancia_valida": "OK",
    "campo_extra": "ERRO",
    "data_ausente": "ERRO",
    "origem_diferente": "ERRO",
    "perfil_tipo_errado": "ERRO",
    "atividade_outro_perfil": "ERRO",
    "documento_grande": "ERRO",
    "cpf_no_texto": "AVISO",
    "arquivo_nao_json": "ERRO",
}


def criar_publicacao(caso, destino):
    destino.mkdir(parents=True, exist_ok=True)
    identificador = "instancia-teste"
    actor_id = "https://ciranda-teste.exemplo.org/actor.json"
    documento = {
        "id": "servico-teste",
        "titulo": "Acolhimento de demonstração",
        "resumo": "Descrição fictícia para teste.",
        "para_quem": "Público de demonstração.",
        "como": "Procure o serviço de demonstração.",
        "contato": "contato fictício",
        "fonte": "Fonte fictícia",
        "link": "https://exemplo.org/servico",
        "onde": "Local fictício",
        "data_conferencia": "14/11/2026",
        "a_confirmar": False,
        "origem_instancia": identificador,
    }
    actor = {
        "@context": ["https://www.w3.org/ns/activitystreams"],
        "id": actor_id,
        "type": "Organization",
        "preferredUsername": identificador,
        "name": "Instância de teste",
        "summary": "Catálogo fictício de teste",
        "url": "https://ciranda-teste.exemplo.org",
    }
    outbox = {
        "@context": ["https://www.w3.org/ns/activitystreams"],
        "id": "https://ciranda-teste.exemplo.org/outbox.json",
        "type": "OrderedCollection",
        "totalItems": 1,
        "orderedItems": [{
            "id": actor_id + "#publicacao-servico-teste",
            "type": "Create",
            "actor": actor_id,
            "object": {
                "id": actor_id + "#servico-servico-teste",
                "type": "Note",
                "name": documento["titulo"],
                "summary": documento["resumo"],
                "ciranda:servico": documento,
            },
        }],
    }
    if caso == "campo_extra":
        documento["dado_pessoal"] = "não permitido"
    elif caso == "data_ausente":
        documento["data_conferencia"] = ""
    elif caso == "origem_diferente":
        documento["origem_instancia"] = "outra-instancia"
    elif caso == "perfil_tipo_errado":
        actor["type"] = "Person"
    elif caso == "atividade_outro_perfil":
        outbox["orderedItems"][0]["actor"] = "https://outra.exemplo.org/actor.json"
    elif caso == "documento_grande":
        documento["resumo"] = "x" * 4001
    elif caso == "cpf_no_texto":
        documento["resumo"] = "CPF fictício para teste heurístico: 529.982.247-25"
    elif caso == "arquivo_nao_json":
        (destino / "actor.json").write_text("{ isto não é JSON", encoding="utf-8")
    webfinger = {
        "subject": "acct:{}@ciranda-teste.exemplo.org".format(identificador),
        "links": [{"rel": "self", "type": "application/activity+json", "href": actor_id}],
    }
    (destino / ".well-known").mkdir()
    (destino / ".well-known" / "webfinger").write_text(json.dumps(webfinger), encoding="utf-8")
    if caso != "arquivo_nao_json":
        (destino / "actor.json").write_text(json.dumps(actor), encoding="utf-8")
    (destino / "outbox.json").write_text(json.dumps(outbox), encoding="utf-8")


with tempfile.TemporaryDirectory() as temporario:
    for caso, esperado in CASOS.items():
        descritor = json.loads((PASTA_CASOS / (caso + ".json")).read_text(encoding="utf-8"))
        checar("descritor do caso {}".format(caso), descritor.get("caso") == caso)
        pasta = Path(temporario) / caso
        criar_publicacao(caso, pasta)
        relatorio = verificar_instancia(pasta)
        resultados = [v["resultado"] for v in relatorio["verificacoes"]]
        if esperado == "OK":
            observado = "ERRO" if "ERRO" in resultados else ("AVISO" if "AVISO" in resultados else "OK")
        elif esperado == "AVISO":
            observado = "AVISO" if "AVISO" in resultados and "ERRO" not in resultados else "ERRO"
        else:
            observado = "ERRO" if "ERRO" in resultados else "OK"
        checar("resultado esperado para {}".format(caso), observado == esperado)

# O esquema formal deve espelhar exatamente a lista fechada do conversor.
esquema = json.loads((RAIZ / "ciranda" / "esquema" / "servico.schema.json").read_text(encoding="utf-8"))
checar("campos do esquema idênticos a CAMPOS_PERMITIDOS",
       set(esquema["properties"]) == set(CAMPOS_PERMITIDOS)
       and len(esquema["properties"]) == len(CAMPOS_PERMITIDOS))

# Varredura dos itens reais: os achados são reportados, nunca ocultados.
sys.path.insert(0, str(RAIZ / "MISM2" / "algoritimos"))
import apoio
documentos_reais = converter_catalogo(apoio.ITENS, "catalogo-real")
achados = _achados_privacidade(documentos_reais)
if achados:
    for achado in achados:
        print("AVISO PRIVACIDADE: " + achado)
else:
    print("OK   varredura heurística do catálogo real: nenhum CPF válido ou número de 15 dígitos detectado")
print("Catálogo real: {} itens examinados; {} alerta(s) heurístico(s).".format(len(documentos_reais), len(achados)))
checar("varredura heurística do catálogo real executada", True)

print("Teste de conformidade concluído.")
