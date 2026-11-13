# Como executar a Ciranda

Os comandos abaixo partem da raiz do repositório. O protótipo independente usa apenas os módulos da Ciranda; não precisa iniciar o painel MISM, carregar dados Parquet, abrir banco de dados nem configurar chaves.

## 1. Abrir a demonstração independente

Instale as dependências do projeto a partir do `requirements.txt` da raiz e execute:

```powershell
pip install -r requirements.txt
streamlit run ciranda/app_ciranda.py
```

Na primeira abertura, a aplicação importa automaticamente a instância fictícia localizada em `ciranda/demonstracao/instancia_demo/`. A importação é gravada em `ciranda/importados/`, pasta ignorada pelo Git, e não substitui um arquivo de demonstração que já exista. A faixa no topo informa que os serviços são fictícios.

## 2. Publicar no Streamlit Community Cloud

1. Acesse https://share.streamlit.io/ e entre com sua conta GitHub.
2. Selecione **Create app** e escolha o repositório `vladimirsejas/ciranda-nacional`.
3. Selecione a branch `federacao`.
4. Em **Main file path**, informe exatamente `ciranda/app_ciranda.py`.
5. Em **Advanced settings**, mantenha o arquivo de dependências `requirements.txt` da raiz do repositório (não crie um segundo arquivo de dependências).
6. Publique o aplicativo.

A Ciranda independente não requer Secrets, Gemini, token, chave de API, dados Parquet ou banco de dados. Não cadastre credenciais em **Secrets** para executar este protótipo. O repositório é privado; a implantação depende de o Streamlit Community Cloud ter acesso autorizado ao repositório.

## 3. Gerar os arquivos públicos de uma instância

A publicação usa o manifesto da instância e a lista `ITENS` do catálogo de apoio existente no MISM2. Este comando de publicação é uma ferramenta separada; não é necessário para abrir a demonstração independente:

```powershell
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
```

A pasta de saída contém `.well-known/webfinger`, `actor.json` e `outbox.json`. Publique esses arquivos em hospedagem estática, preservando os caminhos. O endereço HTTPS do manifesto deve corresponder ao endereço público efetivamente usado.

## 4. Importar ou atualizar outra instância

Para seguir uma instância publicada:

```powershell
@'
from ciranda.seguir import seguir_instancia

resultado = seguir_instancia("https://endereco-publico-da-instancia")
print(resultado)
'@ | python
```

Para testes locais, passe a pasta que contém `actor.json` e `outbox.json`:

```powershell
@'
from ciranda.seguir import seguir_instancia

resultado = seguir_instancia("publicacao", "ciranda/importados")
print(resultado)
'@ | python
```

Cada instância seguida gera um arquivo separado em `ciranda/importados/`, ignorado pelo Git. A importação não altera o catálogo local e não sobrescreve automaticamente uma importação existente. A origem e a data de conferência declaradas por quem publicou são mantidas; o item não é marcado como verificado localmente.

Na página **Rede Ciranda**, use o botão **Atualizar** da instância desejada. A versão recebida é validada antes da troca; a versão anterior é guardada em `ciranda/importados/historico/`. Se a atualização falhar, o arquivo atual permanece intacto.

A leitura remota exige HTTPS, recusa localhost, IPs numéricos e nomes que resolvam para endereços privados ou reservados. O IP público resolvido é usado na conexão. Cada resposta tem limite de 2 MB, a lista aceita até 500 serviços e cada campo textual tem limite de 4.000 caracteres.

Textos recebidos são apresentados sem interpretação de Markdown ou HTML. Links são exibidos com seu domínio e o aviso: **Link informado por outra instância; confira antes de usar**.

## 5. Testes

Execute os testes novos individualmente:

```powershell
python testes/teste_ciranda_instancia.py
python testes/teste_ciranda_servico.py
python testes/teste_ciranda_publicar.py
python testes/teste_ciranda_seguir.py
python testes/teste_ciranda_seguranca.py
python testes/teste_ciranda_tela.py
python testes/teste_ciranda_app.py
```

Os testes legados relacionados ao catálogo e à tela de Apoio podem ser executados com:

```powershell
python MISM2/algoritimos/teste_apoio.py
python MISM2/dashboard/teste_apoio_tela.py
```

O formato de publicação contém extensões locais identificadas como **A VERIFICAR**. A geração e a leitura estática não demonstram, por si só, compatibilidade com outras implementações ActivityPub.
