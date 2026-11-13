"""Publicação estática, somente de leitura, inspirada em ActivityStreams."""
import json
from pathlib import Path
from urllib.parse import urlparse

from ciranda.instancia import validar_manifesto
from ciranda.servico import converter_catalogo


def _json(caminho, dados):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def gerar_arquivos(manifesto, catalogo, pasta_saida):
    """Gera .well-known/webfinger, actor.json e outbox.json para hospedagem estática."""
    erros = validar_manifesto(manifesto)
    if erros:
        raise ValueError("Manifesto inválido:\n- " + "\n- ".join(erros))
    if not isinstance(catalogo, (list, tuple)):
        raise ValueError("O catálogo deve ser uma lista de itens.")
    base = manifesto["endereco_publico"].rstrip("/")
    host = urlparse(base).netloc
    identificador = manifesto["identificador"]
    actor_url = base + "/actor.json"
    outbox_url = base + "/outbox.json"
    webfinger = {
        "subject": "acct:{}@{}".format(identificador, host),
        "links": [{
            "rel": "self",
            "type": "application/activity+json",
            "href": actor_url,
        }],
    }
    # Subconjunto estático de leitura. Não há inbox, chaves, assinaturas ou promessa de federação compatível.
    actor = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": actor_url,
        "type": "Organization",
        "preferredUsername": identificador,
        "name": manifesto["nome"],
        "summary": "Instância Ciranda. Publica somente catálogo público de serviços de apoio.",
        "url": base,
        "outbox": outbox_url,
        "ciranda:tipo": manifesto["tipo"],
        "ciranda:contatoPublico": manifesto["contato_publico"],
    }
    documentos = converter_catalogo(catalogo, identificador)
    atividades = []
    for documento in documentos:
        servico_id = documento["id"]
        objeto = {
            "id": actor_url + "#servico-" + servico_id,
            # A VERIFICAR: tipo Service e propriedades ciranda:* são extensões locais; não se afirma compatibilidade.
            "type": "Note",
            "name": documento["titulo"],
            "summary": documento["resumo"],
            "ciranda:servico": documento,
        }
        atividades.append({
            "id": actor_url + "#publicacao-" + servico_id,
            "type": "Create",
            "actor": actor_url,
            "object": objeto,
        })
    outbox = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            {"ciranda": "https://ciranda.invalid/ns#"},
        ],
        "id": outbox_url,
        "type": "OrderedCollection",
        "totalItems": len(atividades),
        "orderedItems": atividades,
    }
    saida = Path(pasta_saida)
    _json(saida / ".well-known" / "webfinger", webfinger)
    _json(saida / "actor.json", actor)
    _json(saida / "outbox.json", outbox)
    return {
        "webfinger": str(saida / ".well-known" / "webfinger"),
        "actor": str(saida / "actor.json"),
        "outbox": str(saida / "outbox.json"),
        "total_servicos": len(documentos),
    }
