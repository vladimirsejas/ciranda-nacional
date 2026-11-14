# Especificação da Ciranda — versão 0.1

**Estado:** descrição do comportamento implementado na branch de referência. Esta especificação não declara compatibilidade integral com ActivityPub.

## 1. Publicação de uma instância

A função `ciranda.publicar.gerar_arquivos(manifesto, catalogo, pasta_saida)` grava três arquivos estáticos:

| Caminho relativo | Conteúdo |
|---|---|
| `.well-known/webfinger` | Objeto JSON com `subject` no formato `acct:<identificador>@<host>` e um link `self` do tipo `application/activity+json` apontando para o perfil. |
| `actor.json` | Perfil público da instância. |
| `outbox.json` | Coleção ordenada de atividades de publicação. |

O endereço do perfil é `<endereco_publico>/actor.json`; o da coleção é `<endereco_publico>/outbox.json`. O endereço público do manifesto deve ser HTTPS. A publicação é feita em diretório de saída escolhido por quem executa a função; o código não faz hospedagem.

O perfil tem `@context` com o contexto ActivityStreams e um contexto local `ciranda`, `id`, `type: Organization`, `preferredUsername`, `name`, `summary`, `url`, `outbox`, `ciranda:tipo` e `ciranda:contatoPublico`.

A coleção tem `@context`, `id`, `type: OrderedCollection`, `totalItems` e `orderedItems`. Cada item é uma atividade `Create`, cujo `actor` é o identificador URL do perfil e cujo `object` é do tipo `Note`. O objeto inclui `id`, `name`, `summary` e `ciranda:servico`.

## 2. Documento de serviço

O conversor `ciranda.servico.criar_documento_servico` produz exatamente os 12 campos abaixo. Todos aparecem no documento produzido; campos textuais sem valor na origem são serializados como texto vazio. A importação atual exige explicitamente `id`, `data_conferencia` e `origem_instancia` não vazios; os demais campos permitidos podem estar ausentes em documentos recebidos, embora o publicador da versão atual sempre os gere.

| Campo | Tipo | Obrigatório no documento gerado | Significado |
|---|---|---:|---|
| `id` | texto | Sim | Identificador do item no catálogo de origem. |
| `titulo` | texto | Sim | Título público do serviço. |
| `resumo` | texto | Sim | Resumo público. |
| `para_quem` | texto | Sim | Público a que o item se destina. |
| `como` | texto | Sim | Orientação de acesso descrita no catálogo. |
| `contato` | texto | Sim | Contato público informado no catálogo. |
| `fonte` | texto | Sim | Fonte informada no catálogo. |
| `link` | texto | Sim | Link informado no catálogo. |
| `onde` | texto | Sim | Localização ou abrangência descrita no catálogo. |
| `data_conferencia` | texto | Sim | Data registrada no campo `conferido` do item de origem. |
| `a_confirmar` | booleano | Sim | Verdadeiro quando o item de origem contém texto não vazio em `confirmar`; falso nos demais casos. |
| `origem_instancia` | texto | Sim | Identificador da instância que publicou o documento. |

O conversor usa a lista fechada `CAMPOS_PERMITIDOS`; campos adicionais presentes no item de entrada não são copiados.

## 3. Proveniência e apresentação

- O documento publicado conserva `origem_instancia` e `data_conferencia` declaradas pela instância publicadora.
- A importação cria, ao redor do documento, os campos locais `origem`, `data_conferencia_publicada`, `data_importacao` e `verificado_localmente: false`.
- A instância que importa não transforma a conferência da publicadora em conferência local.
- A interface apresenta a origem e a data publicada e exibe o aviso de que a instância local não verificou o item.
- `a_confirmar` é uma marca do catálogo de origem. A interface informa quando ela está ativa; não representa validação pela instância importadora.

## 4. Privacidade

O conversor só permite os 12 campos listados. Não se deve acrescentar ao documento público dados de pessoa, identificadores pessoais, dados de saúde individual, prontuários, internações individuais, perguntas de usuárias ou dados de autenticação. O código do conversor descarta campos extras, mas não consegue reconhecer informação pessoal inserida indevidamente dentro de um campo textual permitido. A checagem heurística de CPF e Cartão SUS prevista na suíte de conformidade é um alerta, não uma garantia de ausência de dados pessoais.

## 5. Limites implementados na importação

| Limite | Valor | Aplicação |
|---|---:|---|
| Tamanho de cada arquivo/resposta JSON | 2 MiB (2 × 1024 × 1024 bytes) | Arquivos locais e respostas HTTPS de perfil e coleção. |
| Publicações/serviços por instância | 500 | Quantidade de elementos em `orderedItems`. |
| Texto em cada valor textual e chave JSON recebida | 4.000 caracteres | Perfil, envelope da coleção e documentos de serviço. |

O cliente remoto exige HTTPS, rejeita endereços locais e IPs não globais após resolução DNS, fixa a conexão no IP público resolvido, exige HTTP 200 e não segue redirecionamentos automaticamente. Esses controles são implementações do importador, não garantias oferecidas pelo protocolo.

## 6. Relação com ActivityPub e ActivityStreams

Esta versão usa nomes e estruturas inspirados em ActivityStreams: `Organization`, `OrderedCollection`, `Create` e `Note`, além do contexto padrão. As propriedades `ciranda:*` são extensões locais; o próprio código marca o objeto `Note` e essas propriedades como **A VERIFICAR**. Portanto, esta versão não afirma interoperabilidade integral ou conformidade normativa com ActivityPub.

A troca implementada é somente leitura, por arquivos estáticos. Não há `inbox`, entrega de atividades, assinaturas criptográficas, chaves públicas ou autenticação de remetente. O perfil publicado não contém caixa de entrada.

## 7. Versão da especificação

**Implementado atualmente:** o manifesto e o perfil gerados não possuem campo de versão da especificação. Portanto, uma instância ainda não declara formalmente qual versão segue.

**Proposta futura:** acrescentar ao perfil um campo de namespace, por exemplo `ciranda:specificationVersion: "0.1"`, e definir política de compatibilidade e negociação. Esse campo ainda não é produzido nem validado pelo código. A forma final do campo e sua semântica ficam **A VERIFICAR**.
