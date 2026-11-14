# Como testar a Ciranda

No Windows, na raiz do repositório, execute a suíte:

```powershell
py testes\rodar_todos.py
```

Para verificar uma instância publicada localmente ou por HTTPS:

```powershell
py -m ciranda.conformidade "caminho\para\a\instancia"
py -m ciranda.conformidade "https://exemplo.org"
```

O workflow `testes-ciranda.yml` executa em cada push e pull request, prepara Python 3.12, instala as dependências da raiz (com alternativa mínima) e chama `python testes/rodar_todos.py`. O resultado deve ser conferido na aba **Actions** do GitHub.
