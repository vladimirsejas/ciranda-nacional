import os
import sys
import tempfile
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from ciranda.instancia import carregar_manifesto, validar_manifesto


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


valido = {
    "nome": "Ciranda Rio Claro",
    "tipo": "cidade",
    "municipio": "Rio Claro - SP",
    "endereco_publico": "https://ciranda.exemplo.org",
    "contato_publico": "contato@ciranda.exemplo.org",
    "identificador": "rio-claro",
}
checar("manifesto válido", validar_manifesto(valido) == [])
faltando = dict(valido)
del faltando["nome"]
del faltando["municipio"]
checar("campos faltando geram erros claros", len(validar_manifesto(faltando)) >= 2)
invalido = dict(valido, identificador="Rio_Claro")
checar("identificador inválido é rejeitado", any("identificador" in e for e in validar_manifesto(invalido)))
url_invalida = dict(valido, endereco_publico="http://exemplo.org")
checar("endereço sem HTTPS é rejeitado", any("HTTPS" in e for e in validar_manifesto(url_invalida)))
with tempfile.TemporaryDirectory() as pasta:
    caminho = os.path.join(pasta, "manifesto.json")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(valido, arquivo)
    checar("carregador lê manifesto válido", carregar_manifesto(caminho)["identificador"] == "rio-claro")
print("Teste de manifesto concluído.")
