"""Executa todos os testes Ciranda como subprocessos e resume seus resultados."""
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
arquivos = sorted(glob.glob(str(RAIZ / "testes" / "teste_ciranda_*.py")))
linhas = []
falha_geral = False

for arquivo in arquivos:
    inicio = time.monotonic()
    try:
        processo = subprocess.run(
            [sys.executable, arquivo],
            cwd=str(RAIZ),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=240,
        )
        saida = (processo.stdout or "") + "\n" + (processo.stderr or "")
        ok = sum(1 for linha in saida.splitlines() if linha.strip().startswith("OK"))
        falhou = sum(1 for linha in saida.splitlines() if linha.strip().startswith("FALHOU"))
        if processo.returncode != 0 and falhou == 0:
            falhou = 1
        if processo.returncode != 0 or falhou:
            falha_geral = True
        linhas.append((Path(arquivo).name, ok, falhou, time.monotonic() - inicio))
        if processo.returncode != 0:
            print("ERRO DE PROCESSO — {} (código {})".format(Path(arquivo).name, processo.returncode))
            print(saida[-6000:])
    except subprocess.TimeoutExpired:
        falha_geral = True
        linhas.append((Path(arquivo).name, 0, 1, time.monotonic() - inicio))
        print("TIMEOUT — {}".format(Path(arquivo).name))
    except Exception as erro:
        falha_geral = True
        linhas.append((Path(arquivo).name, 0, 1, time.monotonic() - inicio))
        print("ERRO — {}: {}".format(Path(arquivo).name, erro))

print("\n{:<38} {:>7} {:>9} {:>10}".format("ARQUIVO", "OK", "FALHOU", "TEMPO(s)"))
print("-" * 68)
for nome, ok, falhou, tempo in linhas:
    print("{:<38} {:>7} {:>9} {:>10.2f}".format(nome, ok, falhou, tempo))
print("-" * 68)
print("Total: {} arquivo(s) de teste.".format(len(linhas)))
if not arquivos:
    print("Nenhum teste teste_ciranda_*.py foi encontrado.")
    sys.exit(1)
sys.exit(1 if falha_geral else 0)
