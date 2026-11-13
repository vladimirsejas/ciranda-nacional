# Progresso da Ciranda

Branch de trabalho: `federacao`, criada a partir de `main`. Nenhuma alteração é feita diretamente em `main`.

## Regras de segurança e escopo

- Repositório exclusivo: `vladimirsejas/ciranda-nacional`.
- MISM, MISM2 independente e MISM3 permanecem intocados.
- Dados federados: somente catálogo público de serviços de apoio, derivado de `MISM2/algoritimos/apoio.py` (`ITENS`).
- Não federar pessoas, dados pessoais ou internações individuais.
- Serviço externo sempre conserva origem e data de conferência declaradas pela instância publicadora; nunca é apresentado como verificado localmente.
- Código novo da Ciranda fica em `ciranda/`. Nenhum arquivo local ou cópia é criado no computador do usuário.
- Não foi escolhida licença.

## Execução

### Comando 1 — identidade da instância

- [x] Branch `federacao` criado a partir de `main`.
- [x] `ciranda/instancia.py`: manifesto, carregamento e validação em português.
- [x] `ciranda/instancia.exemplo.json`: exemplo de Rio Claro.
- [x] `testes/teste_ciranda_instancia.py`.
- Teste: **NÃO EXECUTADO**.

### Comando 2 — serviço federável

- [x] `ciranda/servico.py`: documento JSON com lista fechada de campos permitidos, origem e data de conferência.
- [x] Campos extras do item de origem são descartados; `confirmar` vira `a_confirmar` booleano.
- [x] `testes/teste_ciranda_servico.py`: cobre todos os itens reais de `ITENS`, campos permitidos, marca, data, JSON e descarte de campo extra.
- Teste: **NÃO EXECUTADO**.

### Comando 3 — publicar

- [x] `ciranda/publicar.py`: gera WebFinger, perfil `actor.json` e `outbox.json` estáticos.
- [x] Publicação somente de leitura; não há inbox, assinatura ou chave.
- [x] Instância e catálogo fictícios em `ciranda/demonstracao/instancia_demo/`.
- [x] `testes/teste_ciranda_publicar.py`.
- Teste: **NÃO EXECUTADO**.
- Propriedades `ciranda:*` são extensões locais **A VERIFICAR**; não se afirma compatibilidade com outras plataformas.

### Comando 4 — seguir e importar

- [x] `ciranda/seguir.py`: leitura de URL HTTPS ou pasta local, validação de perfil/outbox e rejeição de estrutura inválida.
- [x] Importação em arquivo separado por instância, com origem, data de conferência publicada, data de importação e `verificado_localmente: false`.
- [x] Importação duplicada não sobrescreve arquivo existente.
- [x] `.gitignore` atualizado para ignorar `ciranda/importados/`.
- [x] `testes/teste_ciranda_seguir.py`.
- Teste: **NÃO EXECUTADO**.

### Comando 5 — página no painel

- [x] Página nova `ciranda/paginas/rede_ciranda.py`, mantida dentro de `ciranda/` conforme a regra de localização de todo código novo.
- [x] `app.py` editado para incluir a página Streamlit `Rede Ciranda` em `st.Page` e na navegação. Esta é a alteração existente indispensável para registrar a nova página; as páginas antigas não foram editadas.
- [x] Formulário para seguir endereço HTTPS, lista de instâncias importadas, selo com nome/identificador de origem e data declarada, e aviso explícito de que a instância local não verificou o item.
- [x] `testes/teste_ciranda_tela.py` com Streamlit AppTest.
- Teste de tela: **NÃO EXECUTADO**.

### Comando 6 — fechamento

- [x] `docs/CIRANDA_COMO_RODAR.md`: publicação, importação, abertura da página e comandos de teste.
- [x] Testes novos e legados identificados para execução; todos permanecem **NÃO EXECUTADO**:
  - `testes/teste_ciranda_instancia.py`
  - `testes/teste_ciranda_servico.py`
  - `testes/teste_ciranda_publicar.py`
  - `testes/teste_ciranda_seguir.py`
  - `testes/teste_ciranda_tela.py`
  - `MISM2/algoritimos/teste_apoio.py`
  - `MISM2/dashboard/teste_apoio_tela.py`
- [x] Pull request **#1** aberto de `federacao` para `main`, sem merge: https://github.com/vladimirsejas/ciranda-nacional/pull/1

## Limitações de execução

O acesso de trabalho nesta sessão é pelo conector GitHub, que permite ler e gravar arquivos, mas não executar Python nem Streamlit. Por isso, nenhum teste foi declarado como aprovado; todos permanecem **NÃO EXECUTADO** até uma execução real.
