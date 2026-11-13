# Limpeza da Ciranda — registro

Branch `limpeza` (a partir de `federacao`, ponta `f03844e`); tag `antes-da-limpeza` no ponto de partida.
Cada teste é um script (`python teste_x.py`), executado no diretório de trabalho do CI herdado (`MISM2/.github/workflows/testes.yml`); se falha ali, tenta o diretório alternativo. Ambiente: Python 3.13, dependências do `requirements.txt` + `pytest` (não usado).

## Comandos 7 e 8

Conferidos em `docs/PROGRESSO_CIRANDA.md` (branch `federacao`): comando 7 (ponto de entrada independente) e comando 8 (segurança e atualização) estão incorporados. O PROGRESSO_CIRANDA registra seus testes como "NÃO EXECUTADO"; a linha de base abaixo é a primeira execução real.

## Linha de base (antes de qualquer remoção): 58 de 64 testes passaram

| Teste | Resultado | s | Observação |
|---|---|---|---|
| `MISM2/algoritimos/teste_alcance.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_apoio.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_apoio_busca.py` | passou | 3.4 |  |
| `MISM2/algoritimos/teste_apoio_cancer.py` | passou | 3.9 |  |
| `MISM2/algoritimos/teste_assistente.py` | passou | 28.5 |  |
| `MISM2/algoritimos/teste_busca_caixa.py` | passou | 1.1 |  |
| `MISM2/algoritimos/teste_comparar.py` | passou | 0.6 |  |
| `MISM2/algoritimos/teste_conferir_links.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_conversa.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_conversa_apoio.py` | passou | 1.2 |  |
| `MISM2/algoritimos/teste_entendimento.py` | passou | 1.7 |  |
| `MISM2/algoritimos/teste_fluxo.py` | passou | 1.0 |  |
| `MISM2/algoritimos/teste_glossario.py` | passou | 1.0 |  |
| `MISM2/algoritimos/teste_hospitais_oncologia.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_hospital.py` | passou | 1.3 |  |
| `MISM2/algoritimos/teste_inteligencia.py` | passou | 1.5 |  |
| `MISM2/algoritimos/teste_lia.py` | passou | 2.8 |  |
| `MISM2/algoritimos/teste_mapa_lia.py` | FALHOU (rc=1) | 0.8 | falha de asserção já existente ("é texto fixo: a IA não reescreve"), sem relação com a limpeza |
| `MISM2/algoritimos/teste_onde_atendida.py` | passou | 1.1 |  |
| `MISM2/algoritimos/teste_previsao.py` | passou | 1.2 |  |
| `MISM2/algoritimos/teste_resposta_livre.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_sobre_mism.py` | passou | 0.8 |  |
| `MISM2/algoritimos/teste_unidades_saude.py` | passou | 1.1 |  |
| `MISM2/dashboard/teste_apoio_tela.py` | passou | 73.6 |  |
| `MISM2/dashboard/teste_conversa_apoio_tela.py` | passou | 3.0 |  |
| `MISM2/dashboard/teste_fluxo_animado.py` | passou | 1.0 |  |
| `MISM2/dashboard/teste_hospitais_cancer_tela.py` | passou | 3.6 |  |
| `MISM2/dashboard/teste_navegacao.py` | passou | 3.2 |  |
| `MISM2/dashboard/teste_onde_atendida_tela.py` | passou | 3.9 |  |
| `MISM2/dashboard/teste_painel.py` | FALHOU (rc=1) | 284.0 | KeyError 'fluxo_tab_busca' no painel central (falha já existente) |
| `MISM2/dashboard/teste_painel_banco_real.py` | FALHOU (rc=2) | 0.9 | exige o banco real (tabela internacoes), ausente neste ambiente |
| `MISM2/dashboard/teste_perguntas_humano.py` | FALHOU (rc=-9) | 420.1 | excedeu 420 s (exige banco real) |
| `MISM2/etl/teste_baixar_centroides.py` | passou | 0.1 |  |
| `MISM2/etl/teste_baixar_populacao.py` | passou | 0.1 |  |
| `MISM2/etl/teste_baixar_sia_oncologia.py` | passou | 2.0 |  |
| `MISM2/etl/teste_baixar_sih_sp.py` | passou | 2.9 |  |
| `MISM2/etl/teste_baixar_sim_cnes.py` | passou | 0.7 |  |
| `MISM2/etl/teste_carga_duplicidade.py` | passou | 0.4 |  |
| `MISM2/etl/teste_carga_fluxo.py` | passou | 0.7 |  |
| `MISM2/etl/teste_carga_robusta.py` | passou | 0.6 |  |
| `MISM2/etl/teste_carga_territorial.py` | passou | 0.4 |  |
| `MISM2/etl/teste_completude_meses.py` | passou | 0.4 |  |
| `MISM2/etl/teste_consultar_cnes.py` | passou | 0.7 |  |
| `MISM2/etl/teste_criar_tabela_hospitais.py` | passou | 0.1 |  |
| `MISM2/etl/teste_cruzar_hospitais_oncologia.py` | passou | 0.6 |  |
| `MISM2/etl/teste_deteccao_separador.py` | passou | 0.6 |  |
| `MISM2/etl/teste_gerar_hospitais_oncologia_geo.py` | passou | 0.7 |  |
| `MISM2/etl/teste_gerar_lista_hospitais_oncologia.py` | passou | 0.1 |  |
| `MISM2/etl/teste_investigar_2025.py` | passou | 0.5 |  |
| `MISM2/etl/teste_listar_hospitais_por_cidade.py` | passou | 0.0 |  |
| `MISM2/etl/teste_listar_meses_pysus.py` | passou | 0.1 |  |
| `MISM2/etl/teste_selecao_csv.py` | passou | 0.6 |  |
| `MISM2/etl/teste_sondar_mortalidade_geral.py` | passou | 0.5 |  |
| `MISM2/etl/teste_validar_bases_novas.py` | passou | 0.1 |  |
| `testes/teste_ciranda_app.py` | passou | 0.8 |  |
| `testes/teste_ciranda_instancia.py` | passou | 0.1 |  |
| `testes/teste_ciranda_publicar.py` | passou | 0.0 |  |
| `testes/teste_ciranda_seguir.py` | passou | 0.1 |  |
| `testes/teste_ciranda_seguranca.py` | passou | 0.1 |  |
| `testes/teste_ciranda_servico.py` | passou | 0.6 |  |
| `testes/teste_ciranda_tela.py` | passou | 0.9 |  |
| `testes/teste_consulta_cep.py` | passou | 0.1 |  |
| `testes/teste_estudo_rio_claro.py` | FALHOU (rc=1) | 0.5 | scipy não instalado (não está no requirements.txt) |
| `testes/teste_mapa_parquet.py` | FALHOU (rc=1) | 0.5 | exige dados_parquet/aih/aih_rio_claro_geo.parquet, ausente |

## Regra de decisão

Grafo de importações por `ast` (`import`/`from`, inclusive dentro de funções), com pontos de entrada `app.py` (após a limpeza), `MISM2/dashboard/pages/apoio.py`, tudo em `ciranda/` e os testes mantidos; mais busca de nomes de arquivo em strings do código alcançável. Os grupos abaixo registram cada caminho removido/movido, o motivo e o resultado dos testes depois do grupo.

## Grupo A — estudo de Rio Claro e ferramentas territoriais

| Caminho | Ação | Motivo |
|---|---|---|
| `MISM 1/*.py` (calcular_denominadores_usf, calcular_estudo_rio_claro, classificar_areas_usf, consulta_cep, georreferenciar_dados, gerar_mapa) | removido | não alcançáveis a partir do Apoio/ciranda; consulta_cep chamava ViaCEP/BrasilAPI |
| `MISM 1/.gitignore`, `MISM 1/requirements.txt` | removido | só serviam aos scripts removidos |
| `MISM 1/dados/referencia/*.geojson` (2) | removido | só o mapa os lia |
| `MISM 1/readme.md` | movido para `docs/herdado/MISM1_readme.md` | documento herdado |
| `paginas/` (mapa.py, rio_claro.py) | removido | páginas do mapa/estudo; rotas retiradas de `app.py` |
| `testes/teste_consulta_cep.py`, `teste_estudo_rio_claro.py`, `teste_mapa_parquet.py` | removido | só testavam o que saiu (os dois últimos já falhavam na linha de base) |
| `MISM 1/dados/README.md`, `estudo_areas_idade_ajustada.csv`, `estudo_tendencia_por_cancer.csv`, `mulheres_por_area_usf.csv` | **MANTIDO** | lidos por caminho em `MISM2/algoritimos/mism1_conhecimento.py`, importado por `assistente.py`, alcançável pelo Apoio (a Lia explica o mapa com esses agregados) |

Ajustes de links: `assistente.py` perdeu `LINK_MAPA` (apontava para `paginas/mapa.py`; a intenção `mapa_rio_claro` continua respondendo em texto, sem link); `navegacao.py` deixou de acrescentar os botões Mapa/Estudo; `teste_mapa_lia.py` passou a verificar que não há link quebrado.

Testes depois do grupo A (sem os três do painel central, que já falhavam na linha de base e saem no grupo B): **57 de 58 passaram**; a única falha é `teste_mapa_lia.py` ("é texto fixo: a IA não reescreve"), a mesma da linha de base.

## Grupo B — análise de saúde e pipeline de dados

| Caminho | Ação | Motivo |
|---|---|---|
| `MISM2/etl/` (pasta inteira: ~40 scripts de carga/ETL e seus 20 testes) | removido | pipeline de dados do painel; não alcançável do Apoio |
| `MISM2/analises/catalogo_bases_2013_2025.csv`, `controle_qualidade_bases_2013_2025.csv` | removido | nenhum código ou teste mantido os lê |
| `MISM2/analises/base_preditiva_2013_2025.csv` | **MANTIDO: dúvida/dependência** | lido por `teste_inteligencia`, `teste_lia`, `teste_previsao`, `teste_glossario`, `teste_assistente` (testes de módulos que ficam) |
| `MISM2/dashboard/app.py` (painel central), `identidade.py`, `fluxo_animado.py` | removido | painel de análise de saúde; `identidade` só era usado pelo painel |
| `MISM2/dashboard/pages/hospitais_cancer.py`, `pages/onde_ser_atendida.py` | removido | nada mantido depende deles (o Apoio só tinha *links*, ajustados abaixo) |
| `MISM2/dashboard/teste_painel.py`, `teste_painel_banco_real.py`, `teste_perguntas_humano.py`, `teste_fluxo_animado.py`, `teste_hospitais_cancer_tela.py`, `teste_onde_atendida_tela.py`, `teste_navegacao.py` | removido | testavam o painel/páginas removidos (os três primeiros já falhavam na linha de base) |
| `MISM2/algoritimos/passeio.py`, `analise_perguntas.py`, `comparar_regras.py`, `testar_gemini.py` | removido | inalcançáveis; os dois últimos eram ferramentas manuais que chamavam o Gemini |
| `MISM2/algoritimos/onde_atendida.py`, `unidades_saude.py`, `hospitais_oncologia.py` + `teste_busca_caixa.py`, `teste_onde_atendida.py`, `teste_unidades_saude.py`, `teste_hospitais_oncologia.py` | removido | só serviam às páginas removidas |
| `MISM2/dados_geograficos/hospitais_oncologia_{br,br_geo,sp}.csv` | removido | lidos só pelo código removido |
| `MISM2/requirements.txt` | removido | duplicava o `requirements.txt` da raiz |
| `MISM2/.github/workflows/testes.yml` | movido para `docs/herdado/MISM2/testes_ci_herdado.yml` | CI herdado (listava os testes removidos; ficava dentro de MISM2, nunca rodou no GitHub) |
| `MISM2/algoritimos/conversa.py` + `teste_conversa.py` | **MANTIDO** | `teste_entendimento.py` (testa `entendimento`, que fica) compara a caixa nova com `conversa.entender` |
| `MISM2/algoritimos/inteligencia.py`, `assistente.py`, `lia.py`, `mism1_conhecimento.py`, `localizacao.py`, `configuracao_geografica.py` | **MANTIDO** | importados pelo Apoio (`lia`→`inteligencia`; `apoio_busca`→`assistente`→`mism1_conhecimento`/`localizacao`) |
| `MISM2/algoritimos/fonte_parquet.py` | MANTIDO por ora | importado por `configuracao_geografica`; tratado na etapa de rede |
| `MISM2/algoritimos/conferir_links.py` + teste | **MANTIDO** | ferramenta de manutenção prevista (fora das páginas) |
| `MISM2/.gitignore`, `MISM2/.gitattributes`, `MISM2/.streamlit/` | MANTIDO: dúvida | configuração inócua; o `.gitignore` guarda a exceção dos CSV |

Ajustes de links e textos para não apontar para páginas removidas: `app.py` (rotas central/onde/hospitais retiradas; Rede Ciranda é a inicial provisória), botão "🏠 Início" do Apoio e de `navegacao.py` agora voltam ao `app.py` da raiz, a barra de navegação ficou só com "Apoio à mulher", o convite "Ver todos os hospitais habilitados no mapa" do Apoio foi retirado, `LINK_ONDE` removido de `assistente.py`, textos da Lia/glossário que mandavam "ir à página Onde ser atendida" passaram a mandar procurar a UBS, e as notas "cadastro de Onde ser atendida" do catálogo viraram "catálogo de serviços de Rio Claro". Testes ajustados para refletir isso: `teste_apoio_tela.py`, `teste_assistente.py`.

Testes depois do grupo B: **27 de 28 passaram**; a única falha continua sendo `teste_mapa_lia.py` (a mesma da linha de base).

