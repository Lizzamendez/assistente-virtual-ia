# 5. Avaliação e Métricas

## Como o assistente foi avaliado
Foi criado um conjunto de 13 casos de teste em `eval/test_cases.json`:
- **10 perguntas dentro do escopo**, cada uma associada ao `id` do
  registro da base de conhecimento que deveria ser recuperado
  (`expected_id`);
- **3 perguntas fora do escopo** (`expected_id: null`), para verificar
  se o assistente admite corretamente que não tem informação suficiente,
  em vez de "alucinar" uma resposta.

O script `eval/evaluate.py` roda essas perguntas contra o assistente e
calcula:

| Métrica | O que mede |
|---|---|
| **Hit@1** | Nas perguntas dentro do escopo, o tópico correto foi o mais relevante recuperado? |
| **Hit@3** | O tópico correto apareceu entre os 3 mais relevantes recuperados? |
| **Confiança média** | Média da pontuação de similaridade nas perguntas dentro do escopo (quanto maior, mais o modelo "tem certeza"). |
| **Taxa de rejeição correta** | Nas perguntas fora do escopo, em quantas o assistente respondeu corretamente "não sei"? |

## Resultado obtido (última execução)

- **Hit@1:** 9/10 = **90%**
- **Hit@3:** 10/10 = **100%**
- **Confiança média (dentro do escopo):** 0.32
- **Taxa de rejeição correta (fora do escopo):** 2/3 = **67%**

O relatório completo, caso a caso, fica salvo em `eval/report.md` e é
regerado toda vez que `python eval/evaluate.py` é executado.

## O que os erros nos ensinam
Os dois "erros" encontrados não são falhas aleatórias — cada um revela
uma limitação real do modelo de busca lexical (TF-IDF), o que é um
aprendizado importante para o portfólio:

1. **"Como motivar minha equipe de trabalho?"** recuperou primeiro o
   tópico **Direção** (função administrativa) e só em segundo lugar
   **Motivação de Equipes**. Isso faz sentido: os dois textos
   compartilham muito vocabulário ("liderança", "equipe", "motivação").
   Ainda assim, o Hit@3 foi correto, e a resposta final ao usuário
   incluiu ambos os tópicos.
2. **"Qual a receita da minha lasanha de berinjela favorita?"** foi
   incorretamente aceita, porque a palavra "**receita**" tem forte peso
   nos textos de finanças (DRE, fluxo de caixa) — um caso clássico de
   **ambiguidade lexical** que uma busca baseada só em palavras (sem
   entendimento semântico) não resolve sozinha.

## Como isso poderia evoluir
- Trocar/complementar o TF-IDF por **embeddings semânticos** (ex.:
  `sentence-transformers`), que entendem melhor sinônimos e contexto e
  reduziriam esse tipo de falso positivo;
- Aumentar o limiar de confiança (`CONFIDENCE_THRESHOLD` em
  `src/assistant.py`) para ser mais conservador — com o trade-off de
  rejeitar também algumas perguntas legítimas (esse trade-off foi testado
  manualmente durante o desenvolvimento e documentado no código);
- Ampliar a base de casos de teste conforme a base de conhecimento
  crescer, mantendo a avaliação sempre atualizada.
