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
- [x] `testes/teste_ciranda_instancia.py`: manifesto válido, campos ausentes, identificador e URL inválidos.
- Teste: **NÃO EXECUTADO** (o conector GitHub não executa Python).
- Painel não alterado.

### Comando 2 — serviço federável

- [x] `ciranda/servico.py`: documento JSON com lista fechada de campos permitidos, origem e data de conferência.
- [x] Campos extras do item de origem são descartados; `confirmar` vira `a_confirmar` booleano.
- [x] `testes/teste_ciranda_servico.py`: cobre todos os itens reais de `ITENS`, lista permitida, marca, data, JSON e descarte de campo extra.
- Teste: **NÃO EXECUTADO** (o conector GitHub não executa Python).

Dúvidas/decisões: campos textuais ausentes são publicados como texto vazio. O campo interno `levar`, os campos de navegação, metadados de integração e quaisquer campos não listados não são exportados.
