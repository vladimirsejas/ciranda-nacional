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

- [x] `ciranda/instancia.py`, manifesto de exemplo e `testes/teste_ciranda_instancia.py` criados.
- Teste: **NÃO EXECUTADO** (o conector GitHub não executa Python).
- Painel não alterado.

### Comando 2 — serviço federável

- [x] `ciranda/servico.py`: documento JSON com lista fechada de campos permitidos, origem e data de conferência.
- [x] `testes/teste_ciranda_servico.py`: cobre os itens reais de `ITENS`, campos permitidos, marca, data, JSON e descarte de campo extra.
- Teste: **NÃO EXECUTADO**.

### Comando 3 — publicar

- [x] `ciranda/publicar.py`: gera WebFinger, perfil `actor.json` e `outbox.json` estáticos.
- [x] Publicação somente de leitura; não há inbox, assinatura ou chave.
- [x] Instância e catálogo fictícios em `ciranda/demonstracao/instancia_demo/`.
- [x] `testes/teste_ciranda_publicar.py`: valida JSON, perfil, publicações, lista de campos e ausência de campos proibidos.
- Teste: **NÃO EXECUTADO**.

### Comando 4 — seguir e importar

- [x] `ciranda/seguir.py`: leitura de URL HTTPS ou pasta local, validação de perfil/outbox e rejeição de estrutura inválida.
- [x] Importação em arquivo separado por instância, com origem, data de conferência publicada, data de importação e `verificado_localmente: false`.
- [x] Importação duplicada não sobrescreve arquivo existente.
- [x] `.gitignore` atualizado para ignorar `ciranda/importados/` (único arquivo existente alterado até aqui, além do próprio registro de progresso).
- [x] `testes/teste_ciranda_seguir.py`: fluxo A publica/B importa, proveniência, datas, rejeição de inválido e integridade do catálogo local.
- Teste: **NÃO EXECUTADO**.

Dúvidas/decisões: a importação por URL usa HTTPS e consulta `actor.json` e `outbox.json` na raiz do endereço público. O arquivo local de cada instância é criado uma única vez; para atualizar ou substituir uma importação será necessário um procedimento explícito futuro, nunca sobrescrita automática.
