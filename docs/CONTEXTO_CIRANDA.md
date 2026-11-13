# Contexto do projeto Ciranda

## Identidade, origem e relação com o MISM

Ciranda é um projeto novo, mantido no repositório privado `vladimirsejas/ciranda-nacional`, na conta pessoal de Vladimir Queiroz Sejas. Foi criado em 13/11/2026 a partir de uma cópia, com histórico, do repositório MISM. O repositório de origem é [MISM — MISM-Saude-da-Mulher/MISM](https://github.com/MISM-Saude-da-Mulher/MISM), desenvolvido colaborativamente pelo grupo acadêmico.

**O MISM é a integração do MISM1 com o MISM2: MISM = MISM1 + MISM2.** São partes complementares do MISM integrado. Nesta cópia, os conteúdos dessas duas partes aparecem organizados principalmente nos diretórios `MISM 1/` e `MISM2/`. A Ciranda parte do conjunto integrado, preservando seu histórico, e pretende adaptar e ampliar essa base para uma plataforma federada.

Ciranda, entretanto, é um projeto novo e separado. Não é o MISM, não é o repositório independente `vladimirsejas/MISM2` e não é o MISM3 (Rede Mulher, na pasta local `C:\MISM3`). Os projetos de origem continuam independentes e não devem ser alterados durante o trabalho na Ciranda.

## Contexto da chamada FAPESP

A Ciranda está sendo preparada como base de pesquisa e desenvolvimento para a Chamada FAPESP/MCTI/MCom/CGI.br 2026 para Auxílio à Pesquisa Regular (APR) e Projeto Temático, intitulada “Pesquisa e Desenvolvimento de Plataformas Digitais Baseadas em Software Livre e Protocolos Abertos”. A chamada foi anunciada em 15/10/2026 e recebe propostas até 22/02/2027, exclusivamente pelo sistema SAGe.

A chamada busca projetos que estudem, desenvolvam, adaptem ou apliquem plataformas digitais baseadas em software livre e protocolos abertos, especialmente arquiteturas federadas. Entre seus objetivos estão fortalecer infraestruturas digitais abertas e interoperáveis, produzir conhecimento científico e tecnológico, desenvolver soluções e modelos sustentáveis e fortalecer grupos de pesquisa. O Fediverso e o ActivityPub são referências explícitas de arquitetura descentralizada, mas a chamada não obriga que todo projeto use exatamente esse protocolo.

A chamada tem três linhas: (a) desenvolvimento ou aprimoramento de software livre e plataformas descentralizadas; (b) estudos de viabilidade econômica e modelos de negócio; e (c) estudos de impacto socioambiental. O Anexo I cita, entre outros recortes, usabilidade, acessibilidade, interoperabilidade entre plataformas livres, documentação e tutoriais para adoção por pequenos negócios e organizações comunitárias.

A modalidade Auxílio à Pesquisa Regular prevê duração de 2 a 3 anos e orçamento solicitado de até R$ 200 mil por ano. O Projeto Temático prevê 5 anos e até R$ 5 milhões. A chamada incentiva redes com participantes de mais de um estado e parcerias entre academia, setor empresarial e terceiro setor. O software resultante deve usar licença livre reconhecida pela Free Software Foundation ou pela Open Source Initiative. Quando forem solicitados recursos para serviços de terceiros destinados à produção do software, a proposta deve incluir Plano de Gestão de Software de até 3 páginas, cobrindo equipe, funcionalidades, usuários, diferenciação, artefatos, interoperabilidade, testes, documentação, licença, versionamento, distribuição, manutenção, reprodutibilidade e reconhecimento comunitário.

O responsável previsto pela proposta é o Prof. Júlio, doutor e vinculado à Fatec Rio Claro. O grupo de trabalho é formado por estudantes da Fatec. Não há parceria com a Prefeitura. A elegibilidade do proponente, da instituição e da modalidade deve ser conferida conforme as normas da FAPESP; este documento registra o contexto de trabalho e não constitui parecer de elegibilidade.

## Relação entre o MISM e a pesquisa proposta

O MISM integrado (MISM1 + MISM2) já existente é resultado preliminar e fonte de experiência, código, componentes e aprendizados. A FAPESP financia a pesquisa e o desenvolvimento que ainda serão realizados. Portanto, a proposta não deve apresentar o painel atual como se fosse o produto final já financiado: o próximo passo de pesquisa é transformar a base existente numa plataforma federada, aberta, interoperável e adaptável a diferentes contextos.

A Ciranda não deve ser tratada como simples expansão geográfica do painel de Rio Claro. O objetivo é pesquisar e desenvolver uma arquitetura em que diferentes cidades ou organizações possam manter suas próprias instâncias autônomas e interoperar por protocolos abertos.

## Decisão de desenho já tomada

A Ciranda federa **o catálogo de serviços e de apoio às mulheres**, nunca dados de pessoas nem dados individuais de internações.

Cada instância — por exemplo, uma cidade ou uma organização — mantém e publica seus próprios serviços em formato aberto. Outras instâncias podem seguir esses catálogos e apresentar os itens recebidos.

Todo item proveniente de outra instância deve exibir claramente a origem que o publicou e a data de conferência informada por essa origem. Um serviço externo nunca pode aparecer como se tivesse sido verificado ou confirmado pela instância local.

Os dados de saúde permanecem locais. Se futuramente houver compartilhamento, ele será apenas de dados agregados, com supressão de números pequenos conforme a proteção já aplicada no painel de origem. Não federar registros individuais, prontuários, dados pessoais ou internações individualizadas.

A escala nacional será construída pela entrada de novas instâncias de outros estados, e não pela criação de um banco nacional centralizado. Não substituir os arquivos de São Paulo por arquivos nacionais nem converter o banco local em repositório nacional único. A descentralização deve preservar autonomia, responsabilidade e proveniência de cada instância.

## Privacidade e proveniência

- Não transmitir nem federar dados pessoais, identificáveis ou registros individuais de saúde.
- Manter os dados de saúde na instância que os coletou e governa.
- Se houver compartilhamento futuro de indicadores de saúde, transmitir apenas agregados e aplicar supressão de números pequenos.
- Em catálogos federados, preservar origem, autoria institucional e data de conferência declarada pela instância publicadora.
- Não confundir publicação por outra instância com validação local.
- Não centralizar todos os catálogos ou dados de saúde em um banco nacional.
- Não inserir chaves, tokens, segredos, conteúdo de arquivos `.env` ou dados pessoais na documentação.

## Regras de linguagem e prudência herdadas

O arquivo `MISM2/CLAUDE.md` foi localizado e lido. Suas regras de prudência continuam valendo para a documentação e para a futura adaptação: não atribuir causas a associações ou tendências observadas; não apresentar valores hospitalares registrados como orçamento em reais; e descrever projeções como **tendência**, nunca como certeza ou previsão determinística. A inteligência calcula e a camada de linguagem explica sem inventar evidências.

## Limites deste estágio

Este trabalho inicial é apenas de documentação e reconhecimento da base. A classificação de componentes como núcleo reaproveitável não significa que já estejam adaptados, desacoplados ou prontos para federação. Nenhuma mudança de código, teste, dado ou estrutura herdada está autorizada neste estágio. A adaptação para a chamada FAPESP será feita de modo incremental e validado, mantendo a distinção entre componentes potencialmente comuns e conteúdos locais de Rio Claro, do Estado de São Paulo e do SIH/SUS.
