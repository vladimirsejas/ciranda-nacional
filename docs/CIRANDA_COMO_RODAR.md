# Como executar a Ciranda

Os comandos abaixo devem ser executados na raiz do repositório. Use uma instalação Python compatível com as dependências já declaradas no projeto. O manifesto de exemplo usa endereço e contato fictícios: substitua-os por dados públicos reais antes de publicar uma instância.

## 1. Gerar os arquivos públicos de uma instância

A publicação usa o manifesto da instância e a lista \`ITENS\` do catálogo de apoio já existente:

\`\`\`powershell
@'
import sys
sys.path.insert(0, "MISM2/algoritimos")
import apoio
from ciranda.instancia import carregar_manifesto
from ciranda.publicar import gerar_arquivos

manifesto = carregar_manifesto("ciranda/instancia.exemplo.json")
arquivos = gerar_arquivos(manifesto, apoio.ITENS, "publicacao")
print(arquivos)
'@ | python
\`\`\`

A pasta de saída contém \`.well-known/webfinger\`, \`actor.json\` e \`outbox.json\`. Publique esses arquivos em hospedagem estática, preservando os caminhos. O endereço HTTPS do manifesto deve corresponder ao endereço público efetivamente usado.

## 2. Importar serviços de outra instância

Depois que a outra instância publicar os arquivos, importe pelo endereço HTTPS:

\`\`\`powershell
@'
from ciranda.seguir import seguir_instancia

resultado = seguir_instancia("https://endereco-publico-da-instancia")
print(resultado)
'@ | python
\`\`\`

Para testes locais, passe a pasta que contém \`actor.json\` e \`outbox.json\`:

\`\`\`powershell
@'
from ciranda.seguir import seguir_instancia

resultado = seguir_instancia("publicacao", "ciranda/importados")
print(resultado)
'@ | python
\`\`\`

Cada instância seguida gera um arquivo separado em \`ciranda/importados/\`, ignorado pelo Git. A importação não altera o catálogo local e não sobrescreve automaticamente uma importação existente. A origem e a data de conferência declaradas por quem publicou são mantidas; o item não é marcado como verificado localmente.

## 3. Abrir a página Rede Ciranda

Na raiz do projeto:

\`\`\`powershell
streamlit run app.py
\`\`\`

Abra a página **Rede Ciranda** na navegação, informe o endereço HTTPS de outra instância e selecione **Seguir instância**. Os serviços importados aparecem com a origem, a data de conferência publicada e o aviso de que esta instância não verificou o item.

## 4. Testes

Execute os testes novos individualmente:

\`\`\`powershell
python testes/teste_ciranda_instancia.py
python testes/teste_ciranda_servico.py
python testes/teste_ciranda_publicar.py
python testes/teste_ciranda_seguir.py
python testes/teste_ciranda_tela.py
\`\`\`

Os testes legados relacionados ao catálogo e à tela de Apoio podem ser executados com:

\`\`\`powershell
python MISM2/algoritimos/teste_apoio.py
python MISM2/dashboard/teste_apoio_tela.py
\`\`\`

O formato de publicação contém extensões locais identificadas como **A VERIFICAR**. A geração e a leitura estática não demonstram, por si só, compatibilidade com outras implementações ActivityPub.
