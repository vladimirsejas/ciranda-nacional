import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "MISM2", "algoritimos"))
sys.path.insert(0, RAIZ)
import apoio
from ciranda.servico import CAMPOS_PERMITIDOS, converter_catalogo, criar_documento_servico


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


documentos = converter_catalogo(apoio.ITENS, "rio-claro")
checar("todos os itens reais de ITENS foram convertidos", len(documentos) == len(apoio.ITENS))
checar("somente campos da lista fixa são publicados",
       all(set(d).issubset(set(CAMPOS_PERMITIDOS)) for d in documentos))
por_id = {d["id"]: d for d in documentos}
item_confirmar = next(i for i in apoio.ITENS if i.get("confirmar"))
doc_confirmar = por_id[item_confirmar["id"]]
checar("marca a_confirmar é preservada como verdadeiro",
       doc_confirmar["a_confirmar"] is True)
item_data = next(i for i in apoio.ITENS if i.get("conferido"))
checar("data de conferência é preservada",
       por_id[item_data["id"]]["data_conferencia"] == item_data["conferido"])
checar("origem da instância acompanha cada serviço",
       all(d["origem_instancia"] == "rio-claro" for d in documentos))
texto = json.dumps(documentos, ensure_ascii=False)
checar("resultado completo é JSON válido", isinstance(json.loads(texto), list))
com_campo_privado = dict(apoio.ITENS[0], cnes="NAO_PUBLICAR", dado_pessoal="NAO_PUBLICAR")
doc = criar_documento_servico(com_campo_privado, "rio-claro")
checar("campos extras são descartados", "cnes" not in doc and "dado_pessoal" not in doc)
print("Teste de serviço concluído.")
