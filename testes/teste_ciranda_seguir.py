import json
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from ciranda.publicar import gerar_arquivos
from ciranda.seguir import seguir_instancia


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


demo = RAIZ / "ciranda" / "demonstracao" / "instancia_demo"
manifesto = json.loads((demo / "manifesto.json").read_text(encoding="utf-8"))
catalogo = json.loads((demo / "catalogo.json").read_text(encoding="utf-8"))
with tempfile.TemporaryDirectory() as pasta:
    raiz = Path(pasta)
    publicada = raiz / "publicada"
    importados = raiz / "importados"
    catalogo_local = raiz / "catalogo_local.json"
    catalogo_original = '[{"id":"local-intacto"}]\n'
    catalogo_local.write_text(catalogo_original, encoding="utf-8")
    gerar_arquivos(manifesto, catalogo, publicada)
    resultado = seguir_instancia(publicada, importados)
    dados = json.loads(Path(resultado["arquivo"]).read_text(encoding="utf-8"))
    checar("instância B importa todos os serviços publicados por A",
           resultado["total_servicos"] == len(catalogo) == len(dados["servicos"]))
    primeiro = dados["servicos"][0]
    checar("origem do serviço importado é a instância publicadora",
           primeiro["origem"] == "instancia-a-demo"
           and primeiro["servico"]["origem_instancia"] == "instancia-a-demo")
    checar("data de conferência publicada e data de importação são preservadas",
           primeiro["data_conferencia_publicada"] == catalogo[0]["conferido"]
           and bool(primeiro["data_importacao"]))
    checar("serviço importado nunca é marcado como verificado localmente",
           primeiro["verificado_localmente"] is False)
    checar("catálogo local permanece byte a byte inalterado",
           catalogo_local.read_text(encoding="utf-8") == catalogo_original)
    try:
        seguir_instancia(publicada, importados)
        duplicado_rejeitado = False
    except FileExistsError:
        duplicado_rejeitado = True
    checar("importação duplicada não sobrescreve arquivo anterior", duplicado_rejeitado)
    invalida = raiz / "invalida"
    invalida.mkdir()
    (invalida / "actor.json").write_text('{"type":"Organization","id":"https://x.invalid/actor.json","preferredUsername":"x"}', encoding="utf-8")
    (invalida / "outbox.json").write_text('{"type":"Collection","orderedItems":[]}', encoding="utf-8")
    try:
        seguir_instancia(invalida, raiz / "importacao_invalida")
        rejeitada = False
    except ValueError:
        rejeitada = True
    checar("formato inválido é rejeitado com mensagem clara", rejeitada)
print("Teste de importação concluído.")
