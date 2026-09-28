# 3. Prompts

O AdminIA funciona em dois modos (ver `docs/04-aplicacao.md` para detalhes
técnicos), mas em ambos as instruções abaixo orientam o comportamento.

## Prompt de sistema (usado quando a API do Gemini está configurada)

Está definido em `src/llm.py`, na constante `SYSTEM_PROMPT`:

```
Você é o AdminIA, um assistente virtual especialista em Administração de Empresas.

Regras que você deve seguir SEMPRE:
1. Responda apenas com base no CONTEXTO fornecido abaixo. Nunca invente dados, números ou fatos que não estejam no contexto.
2. Se o contexto não for suficiente para responder com segurança, diga claramente que não tem informação suficiente e sugira ao usuário reformular a pergunta ou procurar um especialista humano.
3. Seja direto, claro e didático. Evite jargões sem explicá-los.
4. Sempre que fizer sentido, termine sugerindo um próximo passo prático para a pessoa usuária.
5. Responda sempre em português do Brasil.
```

### Por que esse desenho de prompt (RAG)
O padrão usado é **RAG (Retrieval-Augmented Generation)**: primeiro
buscamos os trechos mais relevantes da base de conhecimento
(`src/kb.py`), depois enviamos **apenas esses trechos** como contexto
para o modelo — nunca deixamos o modelo responder livremente "do zero".
Isso é o que sustenta a regra "evite respostas inventadas" pedida no
desafio: se o contexto não tiver a resposta, a regra 2 do prompt manda o
modelo admitir isso.

## "Prompt" do modo extrativo (fallback sem IA generativa)
Quando não há `GEMINI_API_KEY` configurada (ou o pacote `google-generativeai`
não está instalado), o próprio código (função `_extractive_answer` em
`src/llm.py`) atua como um "prompt determinístico":
ele monta a resposta só com o texto literal da base de conhecimento,
seguindo esta lógica:

1. Se nenhum trecho relevante foi encontrado → devolve a mensagem padrão
   de "não tenho informação suficiente";
2. Se algum trecho foi encontrado → apresenta o tópico principal e,
   se houver, tópicos complementares com boa pontuação;
3. Sempre encerra sugerindo um próximo passo prático.

Esse modo garante que o projeto funcione mesmo sem internet ou chave de
API — importante para um protótipo de portfólio que qualquer avaliador
deve conseguir rodar localmente sem custos.

## Regra de confiança mínima
Antes mesmo de chegar a qualquer prompt, `src/assistant.py` aplica um
filtro de confiança (`CONFIDENCE_THRESHOLD = 0.12`): resultados de busca
abaixo desse limiar de similaridade são descartados e tratados como
"sem informação suficiente". Isso é o que faz o assistente dizer "não
sei" de forma consistente, em vez de depender só do bom senso do modelo
de linguagem.
