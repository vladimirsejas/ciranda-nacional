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

