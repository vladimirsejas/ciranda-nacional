# CLAUDE.md — Ciranda

## O que é
Ciranda é uma plataforma federada de catálogos de serviços de apoio às mulheres (projeto de pesquisa, protótipo).
Nasceu de uma cópia do MISM, mas é um projeto separado: **não é** o MISM, o MISM2 (`vladimirsejas/MISM2`) nem o MISM3.
Nada desses três pode ser tocado. Repositório privado `vladimirsejas/ciranda-nacional`. Sem licença escolhida.

## Desenho já decidido
- Federa **só o catálogo de serviços** (e apoio). Nunca dados de pessoas, prontuários ou internações individuais.
- Cada instância (cidade/organização) publica o próprio catálogo em formato aberto; as outras seguem e exibem.
- **Origem e data de conferência ficam sempre visíveis** em item vindo de outra instância; publicar não é validar.
- Sem banco nacional centralizado: a escala vem da entrada de novas instâncias.
- Dados de saúde, se um dia compartilhados, só como agregados com supressão de números pequenos.

## Regras de linguagem e prudência
- Nada de **causa**: não atribuir causa a associações ou tendências observadas.
- Nada de **orçamento em reais**: valor hospitalar registrado não é orçamento.
- Nada de **"vai acontecer"**: projeção é tendência, nunca certeza.
- A Lia e a busca não dão diagnóstico nem prometem vaga; texto de serviço vem do catálogo conferido.
- Nunca colocar chaves, tokens, `.env` ou dados pessoais em código, docs ou commits.

## Estrutura do repositório
- `app.py` — **único ponto de entrada** (`streamlit run app.py`): Rede Ciranda (inicial) e Apoio à mulher.
- `ciranda/` — federação: `instancia`, `servico`, `publicar`, `seguir` (única rede da federação), `paginas/rede_ciranda.py`, `demonstracao/`.
- `MISM2/dashboard/pages/apoio.py` — página Apoio à mulher; `estilo.py`, `navegacao.py`, `lia_rosto.py`, `lia/` (imagens).
- `MISM2/algoritimos/` — `apoio` (catálogo), `apoio_busca`, `entendimento`, `glossario`, `lia`, e o que eles importam
  (`assistente`, `inteligencia`, `localizacao`, `mism1_conhecimento`, `configuracao_geografica`, `ia_linguagem`, `conversa`);
  `conferir_links.py` é ferramenta de manutenção; `gabarito_*.json` alimentam os testes.
- `MISM2/dados_geograficos/catalogo_servicos_rioclaro.json` — catálogo de Rio Claro.
- `MISM2/analises/base_preditiva_2013_2025.csv`, `MISM 1/dados/referencia/` — dados lidos por módulos/testes mantidos.
- `testes/` — testes da federação e do ponto de entrada. `.streamlit/` — tema.
- `docs/` — contexto, como rodar, mapa do código, `LIMPEZA_CIRANDA.md`; `docs/herdado/` guarda a documentação do MISM.

## Rede e chaves
Só `ciranda/seguir.py` (federação) e `conferir_links.py` (manutenção) tocam a rede. O Gemini do Apoio é opcional:
só existe com `GEMINI_API_KEY` no ambiente/`.env` e a caixa vem desligada por padrão.

## Como rodar os testes
Cada teste é um script (`python arquivo.py`), sem pytest. Dependências: `pip install -r requirements.txt`.
```
python testes/teste_ciranda_app.py            # idem para os outros testes/teste_ciranda_*.py (raiz do repositório)
python MISM2/dashboard/teste_apoio_tela.py    # tela do Apoio (AppTest, ~1 min); rode a partir de MISM2/dashboard
cd MISM2/algoritimos && for t in teste_*.py; do python "$t"; done
```
`teste_mapa_lia.py` falhava antes da limpeza (assertion "é texto fixo: a IA não reescreve") e continua falhando.
Resultados e histórico da limpeza: `docs/LIMPEZA_CIRANDA.md`.

## Git
Sem force push nem reescrita de histórico. Não abrir PR nem fazer merge sem pedido explícito.
