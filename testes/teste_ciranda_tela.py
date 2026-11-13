import os
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from ciranda.paginas.rede_ciranda import carregar_importacoes


def checar(nome, condicao):
    print(("OK   " if condicao else "FALHOU ") + nome)
    if not condicao:
        raise AssertionError(nome)


at = AppTest.from_file(str(RAIZ / "ciranda" / "paginas" / "rede_ciranda.py"), default_timeout=60)
at.run()
checar("página Rede Ciranda abre sem exceções", len(at.exception) == 0)
checar("página apresenta orientação e formulário para seguir instância",
       any("Rede Ciranda" in str(x.value) for x in at.title)
       and any(x.label == "Endereço público da outra instância" for x in at.text_input)
       and any(x.label == "Seguir instância" for x in at.button))
checar("página explica que os serviços vêm de outras instâncias",
       any("responsabilidade de quem publicou" in str(x.value) for x in at.markdown))
checar("leitor de importações vazias retorna lista vazia",
       carregar_importacoes(RAIZ / "ciranda" / "nao_existe_importados") == [])
print("Teste de tela da Rede Ciranda concluído.")
