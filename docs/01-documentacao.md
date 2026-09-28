# 1. Documentação — O que é o AdminIA

## O que o assistente faz
O **AdminIA** é um assistente virtual especialista em **Administração de Empresas**.
Ele responde perguntas sobre conceitos e ferramentas de gestão — finanças,
gestão de pessoas, marketing, estratégia, operações, empreendedorismo e
indicadores de desempenho — usando uma base de conhecimento própria,
organizada e revisada.

## Para quem ele serve
- Estudantes de Administração, Empreendedorismo ou cursos correlatos que
  querem revisar conceitos de forma rápida e conversacional;
- Pequenos empreendedores e gestores que precisam relembrar ou entender
  um conceito de gestão antes de tomar uma decisão (ex.: "o que é ponto
  de equilíbrio?" antes de definir o preço de um produto);
- Qualquer pessoa estudando para uma prova, entrevista ou apresentação
  sobre temas de gestão de negócios.

## Como ele deve se comportar
O AdminIA segue um conjunto claro de regras de comportamento (ver
`docs/03-prompts.md` para o prompt completo):

1. **Nunca inventa informação.** Toda resposta é baseada no conteúdo
   recuperado da base de conhecimento.
2. **Admite quando não sabe.** Se a pergunta estiver fora do escopo da
   base (ex.: "qual o resultado do jogo de ontem?"), ele diz isso
   claramente, em vez de arriscar uma resposta genérica ou inventada.
3. **É didático e direto.** Explica o conceito em linguagem simples e,
   sempre que possível, sugere um próximo passo prático.
4. **Mantém contexto da conversa** através de um histórico simples de
   perguntas e respostas.

## Limites conhecidos (importante ser transparente)
- A base de conhecimento é intencionalmente pequena (protótipo), então
  temas muito específicos ou avançados podem não estar cobertos.
- A busca usa similaridade textual (TF-IDF), o que pode gerar falsos
  positivos quando uma pergunta fora do escopo compartilha palavras com
  algum tópico da base (por exemplo, "qual a **receita** da minha lasanha?"
  pode ser confundido com o tópico de **receita** financeira/DRE — esse
  caso está documentado no relatório de avaliação, `eval/report.md`, como
  uma limitação conhecida do modelo lexical).
- O AdminIA não substitui a orientação de um contador, advogado ou
  consultor especializado para decisões reais de negócio.
