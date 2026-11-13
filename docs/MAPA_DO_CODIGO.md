# Mapa do código — Ciranda

Este inventário classifica o conteúdo versionado presente na cópia do MISM integrado (MISM1 + MISM2). A classificação é preliminar: **NUCLEO** indica potencial de reaproveitamento em outras instâncias, não que o componente já esteja genérico ou pronto para produção. **ESPECIFICO** identifica dependência clara de Rio Claro, do Estado de São Paulo, do SIH/SUS ou de uma página/estudo local. **INCERTO** indica que a finalidade, dependências ou grau de acoplamento precisam de inspeção adicional.

A cópia contém 188 arquivos versionados. Os caminhos abaixo preservam a estrutura que foi encontrada; nenhum arquivo original foi movido, renomeado ou apagado.

## Visão geral

| Área | Classificação predominante | Motivo |
|---|---|---|
| `MISM 1/` | ESPECIFICO | Estudo territorial e mapa de Rio Claro, áreas de USF e dados locais do MISM1. |
| `MISM2/algoritimos/` | MISTA | Há motores, busca, Lia e lógica que podem ser reaproveitados, mas também regras e cálculos epidemiológicos vinculados ao SIH/SUS e SP. |
| `MISM2/dashboard/` | MISTA | Componentes de interface podem inspirar uma experiência comum; páginas e gráficos atuais são do painel local de saúde da mulher. |
| `MISM2/etl/` | MISTA | Há padrões de pipeline reaproveitáveis, mas as cargas atuais conhecem bases e recortes do SUS/SP. |
| `MISM2/dados_geograficos/` e `MISM2/analises/` | ESPECIFICO | Catálogos, recortes geográficos e bases de análise já produzidos para o MISM de origem. |
| `MISM2/docs/` | MISTA | Documenta decisões técnicas úteis e também o domínio, os dados e a interface do projeto original. |
| Raiz (`app.py`, `paginas/`, `testes/`) | MISTA | Estrutura do site e testes trazem padrões técnicos reaproveitáveis, mas páginas atuais exibem estudos locais. |

## Raiz do repositório

| Caminho | Classe | Motivo |
|---|---|---|
| `app.py` | NUCLEO | Ponto de entrada Streamlit do site; a estrutura de inicialização pode informar uma arquitetura de instâncias. |
| `paginas/mapa.py` | ESPECIFICO | Página de mapa baseada no conteúdo geográfico herdado do MISM1. |
| `paginas/rio_claro.py` | ESPECIFICO | Página explicitamente dedicada ao estudo de Rio Claro. |
| `testes/teste_consulta_cep.py` | ESPECIFICO | Testa consulta e fluxo de CEP do estudo geográfico de origem. |
| `testes/teste_estudo_rio_claro.py` | ESPECIFICO | Testa cálculos e resultados do estudo de Rio Claro. |
| `testes/teste_mapa_parquet.py` | INCERTO | Testa integração de mapa e Parquet; a parte de persistência pode ser reaproveitável, mas o conteúdo parece local. |
| `requirements.txt` | INCERTO | Dependências da aplicação atual; a seleção precisa ser refeita para a arquitetura alvo da Ciranda. |
| `preparar_dados_deploy.py` | INCERTO | Preparação de dados para implantação do site original; precisa ser reavaliada para implantação federada. |
| `FONTES_DOS_DADOS.md` | ESPECIFICO | Registra proveniência de bases usadas pelo MISM original, incluindo recortes locais e de saúde. |
| `HOSPEDAR.md` | INCERTO | Instruções de hospedagem podem conter escolhas específicas do deploy atual. |
| `LEIAME.md` | INCERTO | Documento informativo do projeto original; não é especificação da Ciranda. |
| `PROGRESSO.md` | INCERTO | Registro de andamento do MISM de origem, não necessariamente estado atual da Ciranda. |
| `README.md` | INCERTO | README herdado foi substituído nesta etapa por uma apresentação curta da Ciranda. |
| `SITE.bat` | INCERTO | Atalho operacional do site no ambiente original; não é componente de produção. |
| `Abrir MISM.bat` | INCERTO | Atalho operacional herdado; não é componente reutilizável de uma plataforma hospedada. |
| `.streamlit/config.toml` | NUCLEO | Configuração de interface Streamlit, reaproveitável como referência e sujeita à configuração por instância. |
| `.devcontainer/devcontainer.json` | NUCLEO | Configuração de ambiente de desenvolvimento, potencialmente útil para reprodutibilidade. |
| `.gitignore` | NUCLEO | Regras de exclusão do Git podem ser aproveitadas após revisão para a nova estrutura. |

## MISM1 — diretório `MISM 1/`

| Caminho | Classe | Motivo |
|---|---|---|
| `MISM 1/` | ESPECIFICO | Conjunto de scripts do estudo territorial do MISM1. |
| `MISM 1/calcular_denominadores_usf.py` | ESPECIFICO | Calcula denominadores ligados às áreas de USF de Rio Claro. |
| `MISM 1/calcular_estudo_rio_claro.py` | ESPECIFICO | Executa cálculos do estudo municipal de Rio Claro. |
| `MISM 1/classificar_areas_usf.py` | ESPECIFICO | Classificação territorial por áreas de USF do município estudado. |
| `MISM 1/consulta_cep.py` | INCERTO | Consulta de CEP pode ser útil em outros contextos, mas precisa de revisão de privacidade e dependência de provedor. |
| `MISM 1/georreferenciar_dados.py` | INCERTO | Georreferenciamento pode ser componente técnico comum, mas o fluxo atual está associado ao estudo local e a dados sensíveis. |
| `MISM 1/gerar_mapa.py` | ESPECIFICO | Gera mapa temático do estudo de Rio Claro e suas áreas de USF. |
| `MISM 1/dados/README.md` | ESPECIFICO | Explica dados de referência do estudo territorial original. |
| `MISM 1/dados/referencia/estudo_areas_idade_ajustada.csv` | ESPECIFICO | Agregado analítico do estudo local por área e idade. |
| `MISM 1/dados/referencia/estudo_tendencia_por_cancer.csv` | ESPECIFICO | Série de tendência por câncer do recorte municipal/estadual do estudo. |
| `MISM 1/dados/referencia/mulheres_por_area_usf.csv` | ESPECIFICO | Denominadores locais por área de USF. |
| `MISM 1/dados/referencia/mapaRioClaroUSF.geojson` | ESPECIFICO | Geometria territorial das áreas de USF de Rio Claro. |
| `MISM 1/dados/referencia/municipio_rio_claro.geojson` | ESPECIFICO | Limite geográfico do município de Rio Claro. |
| `MISM 1/readme.md` | ESPECIFICO | Documentação do estudo MISM1 e seus dados locais. |
| `MISM 1/requirements.txt` | INCERTO | Dependências de scripts cartográficos específicos; avaliar antes de incorporar ao ambiente comum. |
| `MISM 1/.gitignore` | NUCLEO | Regras Git locais podem servir de referência após consolidação. |

## MISM2 — motores, busca, catálogo e lógica

| Caminho | Classe | Motivo |
|---|---|---|
| `MISM2/algoritimos/lia.py` | NUCLEO | Árvore de orientação e composição de respostas da Lia pode ser separada do domínio e adaptada por instância. |
| `MISM2/algoritimos/apoio.py` | INCERTO | Contém catálogo e caminhos de apoio oncológico e à mulher; a estrutura é útil, mas muitos itens e regras são específicos de SP. |
| `MISM2/algoritimos/apoio_busca.py` | NUCLEO | Busca e recuperação sobre catálogo são padrões reaproveitáveis, desde que o índice e os dados sejam locais à instância. |
| `MISM2/algoritimos/assistente.py` | INCERTO | Orquestra respostas com escopo fortemente associado ao painel de saúde da mulher e precisa de desacoplamento. |
| `MISM2/algoritimos/conversa.py` | NUCLEO | Separação entre entendimento, consulta e explicação é um padrão reaproveitável, após remover dependências de domínio. |
| `MISM2/algoritimos/entendimento.py` | NUCLEO | Interpretação/intenção de perguntas pode ser reutilizada com vocabulários e políticas configuráveis. |
| `MISM2/algoritimos/ia_linguagem.py` | NUCLEO | Camada de linguagem pode ser adaptada como serviço auxiliar, mantendo limites, privacidade e independência de provedor. |
| `MISM2/algoritimos/analise_perguntas.py` | INCERTO | Analisa perguntas registradas; revisar necessidade, retenção e privacidade antes de reutilizar. |
| `MISM2/algoritimos/comparar_regras.py` | INCERTO | Comparação de regras aparenta apoiar validação do domínio atual; precisa de inspeção antes de generalizar. |
| `MISM2/algoritimos/conferir_links.py` | NUCLEO | Verificação automatizada de links de catálogo pode ser reutilizada com escopo por instância. |
| `MISM2/algoritimos/configuracao_geografica.py` | INCERTO | Configuração territorial é relevante para instâncias, mas a implementação herdada contém pressupostos do painel e do SIH. |
| `MISM2/algoritimos/fonte_parquet.py` | NUCLEO | Adaptador de leitura de Parquet e montagem de banco é um padrão de acesso a dados potencialmente reutilizável. |
| `MISM2/algoritimos/glossario.py` | INCERTO | Vocabulário atual é de saúde da mulher e câncer; a estrutura pode servir, mas os termos são específicos. |
| `MISM2/algoritimos/hospitais_oncologia.py` | ESPECIFICO | Regras e catálogo de hospitais oncológicos estão vinculados ao SUS e à rede brasileira/paulista. |
| `MISM2/algoritimos/inteligencia.py` | ESPECIFICO | Motor central de indicadores, séries e tendências depende de internações SIH/SUS e recortes territoriais do MISM. |
| `MISM2/algoritimos/localizacao.py` | INCERTO | Funções geográficas podem ser comuns, mas requerem revisão de precisão, privacidade e acoplamento municipal. |
| `MISM2/algoritimos/mism1_conhecimento.py` | ESPECIFICO | Integra conhecimento agregado do estudo MISM1 e de Rio Claro à Lia. |
| `MISM2/algoritimos/onde_atendida.py` | INCERTO | Consulta serviços e unidades, mas combina CNES e catálogo local; separar mecanismo genérico dos dados de cada instância. |
| `MISM2/algoritimos/passeio.py` | INCERTO | Fluxo guiado da interface pode ser reaproveitável, mas destinos e conteúdo pertencem ao painel original. |
| `MISM2/algoritimos/unidades_saude.py` | ESPECIFICO | Leitura e classificação atuais são orientadas ao CNES e à rede de saúde brasileira. |

### Testes e arquivos auxiliares de algoritimos

| Caminho ou grupo | Classe | Motivo |
|---|---|---|
| `MISM2/algoritimos/teste_*.py` (todos os testes sob `MISM2/algoritimos/`) | MISTA | São referência de comportamento; testes de motores genéricos podem ser migrados, enquanto os de SIH, CNES, câncer e Rio Claro ficam como testes do legado. |
| `MISM2/algoritimos/gabarito_*.json` | INCERTO | Gabaritos registram perguntas e respostas do assistente original; revisar conteúdo e dados antes de reutilizar. |

## MISM2 — interface e páginas

| Caminho | Classe | Motivo |
|---|---|---|
| `MISM2/dashboard/app.py` | ESPECIFICO | Painel epidemiológico com abas e indicadores do MISM, baseado em SIH/SUS. |
| `MISM2/dashboard/estilo.py` | NUCLEO | Tokens e padrões visuais podem inspirar uma interface comum, desde que tema e acessibilidade sejam configuráveis. |
| `MISM2/dashboard/identidade.py` | INCERTO | Identidade visual atual representa a experiência do painel original e deve ser desacoplada da identidade Ciranda. |
| `MISM2/dashboard/navegacao.py` | NUCLEO | Padrões de navegação e composição de páginas podem ser reaproveitados. |
| `MISM2/dashboard/lia_rosto.py` | INCERTO | Componente de apresentação da Lia é reutilizável em parte, mas a personagem e suas imagens fazem parte da identidade atual do MISM. |
| `MISM2/dashboard/lia/` | ESPECIFICO | Imagens de expressões da Lia do projeto original; não são conteúdo neutro de plataforma. |
| `MISM2/dashboard/fluxo_animado.py` | INCERTO | Visualização de fluxo pode ser componente comum, mas o fluxo atual representa a rede hospitalar de saúde. |
| `MISM2/dashboard/pages/apoio.py` | ESPECIFICO | Página de apoio com conteúdo, serviços e legislação do contexto paulista/brasileiro atual. |
| `MISM2/dashboard/pages/hospitais_cancer.py` | ESPECIFICO | Página da rede hospitalar oncológica do SUS. |
| `MISM2/dashboard/pages/onde_ser_atendida.py` | INCERTO | Interface de serviços pode inspirar o catálogo federado, mas está acoplada a CNES e ao catálogo de Rio Claro. |
| `MISM2/dashboard/teste_*.py` (todos os testes sob `MISM2/dashboard/`) | MISTA | Testam interação e navegação; cenários do painel e da rede de câncer são específicos, enquanto padrões de navegação podem ser adaptados. |

## MISM2 — ETL e dados

| Caminho ou grupo | Classe | Motivo |
|---|---|---|
| `MISM2/etl/carga_todas_bases.py` | ESPECIFICO | Consolida bases de saúde do MISM e regras territoriais do SIH/SUS. |
| `MISM2/etl/baixar_sih_sp.py` | ESPECIFICO | Coleta e filtra internações hospitalares de São Paulo. |
| `MISM2/etl/baixar_sia_oncologia.py` | ESPECIFICO | Coleta procedimentos oncológicos ambulatoriais do SUS. |
| `MISM2/etl/baixar_sim_obitos.py` | ESPECIFICO | Coleta mortalidade do SIM e regras de residência/UF para o estudo de saúde. |
| `MISM2/etl/baixar_cnes_capacidade.py`, `consultar_cnes.py`, `diagnosticar_*cnes*.py` | ESPECIFICO | Ferramentas de extração e inspeção de estabelecimentos e serviços CNES. |
| `MISM2/etl/criar_tabela_municipios.py` | INCERTO | Catálogo IBGE é útil em várias instâncias, mas esquema e uso estão ligados ao banco do MISM. |
| `MISM2/etl/completude_meses.py` | NUCLEO | Controle explícito de completude temporal é padrão genérico importante para pipelines de dados. |
| `MISM2/etl/exportar_banco_parquet.py` | NUCLEO | Exportação para formato aberto e portável pode ser reutilizada após definir contrato de dados por instância. |
| `MISM2/etl/validar_banco.py`, `validar_bases_novas.py` | NUCLEO | Validação de integridade e qualidade é padrão reaproveitável, com regras de domínio configuráveis. |
| `MISM2/etl/baixar_centroides.py`, `baixar_populacao.py`, `criar_tabela_hospitais.py`, `cruzar_hospitais_oncologia.py`, `gerar_hospitais_oncologia_geo.py`, `gerar_lista_hospitais_oncologia.py`, `listar_hospitais_por_cidade.py` | ESPECIFICO | Scripts orientados a geografia, população e rede hospitalar do recorte de saúde do MISM. |
| `MISM2/etl/carregar_tudo_pysus.py`, `explorar_pysus.py`, `listar_meses_pysus.py`, `sondar_mortalidade_geral.py`, `investigar_2025.py` | ESPECIFICO | Ferramentas de exploração e diagnóstico do PySUS e das bases SIH/SIM/SIA. |
| `MISM2/etl/teste_*.py` (todos os testes sob `MISM2/etl/`) | ESPECIFICO | Testes exercitam downloads, conversões e regras específicas das bases do SUS usadas pelo MISM. |
| `MISM2/analises/` | ESPECIFICO | Bases CSV de análise e controle de qualidade referentes ao período e recorte do estudo original. |
| `MISM2/dados_geograficos/catalogo_servicos_rioclaro.json` | ESPECIFICO | Catálogo local de serviços de Rio Claro; é referência de conteúdo, não catálogo nacional. |
| `MISM2/dados_geograficos/hospitais_oncologia_*.csv` | ESPECIFICO | Listas e georreferenciamento de hospitais oncológicos de SP/Brasil para o estudo do SUS. |
| `MISM2/requirements.txt` | INCERTO | Dependências da aplicação MISM2; consolidar após separar módulos comuns e locais. |

## Documentação herdada do MISM2

| Caminho ou grupo | Classe | Motivo |
|---|---|---|
| `MISM2/CLAUDE.md` | NUCLEO | Registra regras de prudência e decisões técnicas relevantes; regras de linguagem continuam válidas para a Ciranda. |
| `MISM2/README.md` | ESPECIFICO | Descreve o painel e os usos atuais do MISM2, não a Ciranda. |
| `MISM2/docs/LIA.md`, `IA_DO_ESCUDO.md`, `PLANO_CAIXA_DE_PERGUNTAS.md` | INCERTO | Documentam decisões e arquitetura da Lia do domínio original; úteis como referência, exigem adaptação. |
| `MISM2/docs/FONTE_DOS_DADOS.md`, `DADOS_2013_2025.md`, `BASES_ORIGINAIS_2013_2025.md` | ESPECIFICO | Documentam proveniência, recorte temporal e conteúdo das bases de saúde usadas pelo MISM. |
| `MISM2/docs/INVENTARIO_DO_CODIGO.md`, `INVENTARIO_DO_PAINEL.md` | INCERTO | Inventários são úteis para compreender dependências, mas descrevem versões e decisões do sistema de origem. |
| `MISM2/docs/APOIO_COBERTURA_ONCOLOGICA.md`, `INTEGRACAO_GEOGRAFICA.md`, `ROTEIRO_APRESENTACAO_SECRETARIA.md` e PDF correspondente | ESPECIFICO | Referem-se ao conteúdo oncológico, à integração geográfica e à apresentação local do MISM. |
| `MISM2/docs/pesquisa_fontes_saude_reutilizacao_mism3.md` | INCERTO | Pesquisa sobre reutilização de fontes do domínio de saúde e relação com outro projeto; contexto não é especificação Ciranda. |
| `MISM2/docs/historico/` | ESPECIFICO | Registros históricos de decisões e interfaces do MISM2. |
| `MISM2/docs/lia_originais/` | ESPECIFICO | Pranchas originais de identidade visual da personagem Lia. |

## Arquivos operacionais e configuração herdados

| Caminho | Classe | Motivo |
|---|---|---|
| `MISM2/.streamlit/config.toml` | NUCLEO | Configuração Streamlit pode orientar protótipos e implantação por instância. |
| `MISM2/.github/workflows/testes.yml` | NUCLEO | Automação de testes é prática comum, mas a matriz deverá acompanhar a arquitetura nova. |
| `MISM2/.gitignore` e `MISM2/.gitattributes` | NUCLEO | Configurações Git podem ser reutilizadas após consolidação e revisão. |
| `MISM2/Abrir Escudo Feminino.bat`, `Atualizar dados do Escudo.bat`, `Testar IA (Gemini).bat` | ESPECIFICO | Atalhos operacionais para o ambiente Windows e para o MISM2 local. |

## Pontos de atenção

1. **Federação de serviços não é federação de dados de saúde.** O mecanismo de catálogo e proveniência é o principal eixo de desenho novo; motores epidemiológicos e cargas SIH/SUS não devem ser tratados como fonte nacional.
2. **MISM1 e MISM2 compõem o MISM integrado.** Os conteúdos em `MISM 1/` e `MISM2/` são as duas partes da base herdada pela Ciranda, não dois novos projetos da Ciranda.
3. **Dados de SP não devem ser substituídos por arquivos nacionais.** Novas instâncias mantêm seus próprios dados e catálogo, sem banco nacional centralizado.
4. **Origem e data de conferência acompanham cada serviço federado.** A instância consumidora não pode apresentar informação remota como verificada localmente.
5. **Este inventário não autoriza alterações.** Nenhum código, teste ou dado foi modificado nesta etapa; as classificações servem apenas para orientar o entendimento da base.
