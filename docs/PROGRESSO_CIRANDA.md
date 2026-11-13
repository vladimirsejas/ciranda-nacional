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

## Comandos 1 a 6 — implementação inicial

- [x] Manifesto, validação, conversor de catálogo, publicação estática, importação isolada, página Rede Ciranda e guia de execução.
- [x] Demonstração fictícia e testes de unidade/tela criados.
- [x] PR #1 aberto para `main`, sem merge.
- Testes novos e legados da etapa inicial: **NÃO EXECUTADOS** (ambiente de trabalho pelo conector GitHub sem execução Python/Streamlit).

## Comando 7 — ponto de entrada independente

- [x] `ciranda/app_ciranda.py`: ponto de entrada Streamlit próprio, ajusta o caminho para a raiz e abre a página Rede Ciranda.
- [x] Não importa módulos do MISM, nem exige banco, Parquet, dados ou chaves; não contém referências a Gemini.
- [x] Perfil e outbox estáticos adicionados à pasta da demonstração; na primeira abertura importa diretamente de `ciranda/demonstracao/instancia_demo/` para `ciranda/importados/`, sem pasta temporária e sem sobrescrever arquivo existente.
- [x] Faixa superior: “Protótipo de pesquisa. Os serviços exibidos são fictícios, de demonstração.”
- [x] `testes/teste_ciranda_app.py`: AppTest do ponto de entrada, demonstração automática, não sobrescrita e isolamento.
- [x] `docs/CIRANDA_COMO_RODAR.md`: comando `streamlit run ciranda/app_ciranda.py` e instruções de implantação Community Cloud (repositório, branch, arquivo principal e requirements da raiz).
- Teste `testes/teste_ciranda_app.py`: **NÃO EXECUTADO**.

## Comando 8 — segurança e atualização

- [x] Respostas remotas limitadas a 2 MB por arquivo.
- [x] Máximo de 500 serviços por publicação.
- [x] Todos os textos do perfil e do envelope, além dos campos de serviço, limitados a 4.000 caracteres; tipos inesperados são rejeitados.
- [x] Recusa localhost, IPs numéricos e DNS que resolva para IP não global; conexão HTTPS usa o IP público validado, sem seguir redirecionamentos automaticamente.
- [x] Conteúdo remoto na página é exibido por componentes de texto simples, sem interpretação de Markdown/HTML.
- [x] Link mostra domínio de destino e o aviso “Link informado por outra instância; confira antes de usar”.
- [x] `atualizar_instancia`: baixa e valida antes de substituir, arquiva a versão anterior e usa troca atômica; em falha de validação, o arquivo atual não é tocado.
- [x] Botão **Atualizar** por instância seguida.
- [x] `testes/teste_ciranda_seguranca.py`: endereço recusado, DNS privado, IP fixado na conexão, resposta acima de 2 MB, limites de 500 serviços e texto, atualização bem-sucedida e falha sem perda.
- [x] `testes/teste_ciranda_tela.py` atualizado: texto Markdown/HTML literal, domínio, aviso e botão Atualizar.
- Testes `testes/teste_ciranda_seguranca.py` e `testes/teste_ciranda_tela.py`: **NÃO EXECUTADOS**.

## Testes pendentes — resultado real

Todos os testes abaixo permanecem **NÃO EXECUTADO**. O conector GitHub permite gravar e ler arquivos, mas não executa Python ou Streamlit nesta sessão.

- `testes/teste_ciranda_instancia.py`
- `testes/teste_ciranda_servico.py`
- `testes/teste_ciranda_publicar.py`
- `testes/teste_ciranda_seguir.py`
- `testes/teste_ciranda_seguranca.py`
- `testes/teste_ciranda_tela.py`
- `testes/teste_ciranda_app.py`
- `MISM2/algoritimos/teste_apoio.py`
- `MISM2/dashboard/teste_apoio_tela.py`

O PR existente deve receber estes commits automaticamente porque sua origem é a branch `federacao`; não foi feito merge.
