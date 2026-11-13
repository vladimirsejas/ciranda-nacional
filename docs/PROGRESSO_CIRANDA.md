# Progresso da Ciranda

Branch de trabalho: `federacao`. O branch foi criado a partir de `main`; nenhuma alteração é feita diretamente em `main`.

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
- Teste: **NÃO EXECUTADO** (não há execução de Python disponível pelo conector GitHub; não afirmar aprovação).
- Não foi alterado o painel.

Dúvidas/decisões: o endereço público do manifesto exige HTTPS. Para uma cidade é obrigatório `municipio`; para organização é obrigatório `organizacao`. O contato é texto público livre; não é usado como credencial.
