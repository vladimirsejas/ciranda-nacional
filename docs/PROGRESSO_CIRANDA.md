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

### Comando 3 — publicar

- [x] `ciranda/publicar.py`: gera WebFinger, perfil `actor.json` e `outbox.json` estáticos.
- [x] Publicação somente de leitura; não há inbox, assinatura ou chave.
- [x] `ciranda/demonstracao/instancia_demo/`: manifesto e catálogo fictícios; todos os títulos dos itens contêm DEMONSTRAÇÃO.
- [x] `testes/teste_ciranda_publicar.py`: valida JSON, perfil, publicações, lista de campos e ausência de chaves proibidas.
- Teste: **NÃO EXECUTADO** (o conector GitHub não executa Python).

Dúvidas/decisões: o formato usa ActivityStreams como estrutura de envelope. As propriedades `ciranda:*` e o objeto `Note` contendo `ciranda:servico` são extensões locais **A VERIFICAR**; não se afirma compatibilidade com outras plataformas. O WebFinger publicado é um arquivo estático, e a hospedagem deverá expô-lo no caminho `.well-known/webfinger`.
