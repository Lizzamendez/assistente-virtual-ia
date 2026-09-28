# 4. Aplicação Funcional

## Arquitetura (visão geral)

```
Pergunta do usuário
        │
        ▼
┌───────────────────┐   busca por similaridade (TF-IDF)
│   src/kb.py        │ ─────────────────────────────────┐
│ KnowledgeBase       │                                   │
└───────────────────┘                                    ▼
        ▲                                    trechos relevantes + score
        │ carrega                                          │
data/knowledge_base.json                                   ▼
                                                ┌───────────────────┐
                                                │   src/llm.py       │
                                                │ generate_answer()  │
                                                │  - com GEMINI_     │
                                                │    API_KEY: usa    │
                                                │    Gemini (RAG)    │
                                                │  - sem chave: modo │
                                                │    extrativo local │
                                                └───────────────────┘
                                                           │
                                                           ▼
                                                 Resposta ao usuário
                                             (src/assistant.py junta tudo
                                              + guarda histórico da conversa)
```

## Como rodar

### Opção A — GitHub Codespaces (recomendado)
1. *(Opcional, para respostas com IA generativa)* Antes de criar o
   Codespace, cadastre sua chave do Gemini como *secret*: no seu
   repositório no GitHub, vá em **Settings → Secrets and variables →
   Codespaces → New repository secret**, com nome `GEMINI_API_KEY` e o
   valor da chave gerada em https://aistudio.google.com/apikey. Sem essa
   chave, o assistente funciona normalmente no modo extrativo local;
2. No GitHub, clique em **Code → Codespaces → Create codespace on main**;
3. Aguarde o `postCreateCommand` instalar as dependências automaticamente
   (definido em `.devcontainer/devcontainer.json`) — o Codespace já
   recebe o secret cadastrado como variável de ambiente automaticamente;
4. No terminal do Codespaces, rode:
   ```bash
   cd src
   python cli.py
   ```

### Opção B — Localmente

```bash
# 1. Instalar dependências (a única obrigatória é scikit-learn)
pip install -r requirements.txt

# 2. (Opcional) habilitar respostas geradas por IA (Gemini)
export GEMINI_API_KEY="sua-chave-aqui"

# 3. Rodar o chat interativo no terminal
cd src
python cli.py
```

Exemplo de sessão:

```
Você: o que é ponto de equilíbrio?

AdminIA: Sobre Ponto de Equilíbrio (Gestão Financeira):
Ponto de equilíbrio é o volume de vendas necessário para que a receita
cubra exatamente os custos totais (fixos + variáveis), sem lucro nem
prejuízo. Fórmula simplificada: Ponto de Equilíbrio = Custos Fixos /
(Preço de Venda - Custo Variável Unitário). Vender acima desse ponto
gera lucro.

Próximo passo sugerido: anote esse conceito e tente aplicá-lo a um
exemplo real do seu negócio ou estudo de caso para fixar o aprendizado.

   [tópicos usados: Ponto de Equilíbrio | confiança: 0.42]
```

## Uso programático (sem CLI)

```python
from assistant import AdminIAAssistant

bot = AdminIAAssistant()
resposta = bot.ask("Como motivar minha equipe?")
print(resposta["answer"])
print(resposta["had_enough_info"])  # True/False
print(resposta["confidence"])       # 0.0 a 1.0
```

## Por que dois modos de geração (com e sem IA generativa)?
Um assistente "bem funcional" de portfólio precisa rodar em qualquer
máquina (ou Codespace), sem exigir que o avaliador tenha uma chave de API
paga. Por isso o projeto foi desenhado com uma camada de abstração
(`src/llm.py: generate_answer`) que:

- Usa o **Gemini (Google AI API)** para gerar respostas mais fluidas e
  naturais, sempre restritas ao contexto recuperado (RAG de verdade),
  **se e somente se** `GEMINI_API_KEY` estiver definida;
- Cai automaticamente em um **modo extrativo determinístico**, que monta
  a resposta só com o texto da base, sem qualquer dependência externa.

Isso também torna o projeto mais fácil de testar e avaliar de forma
reprodutível (o modo extrativo é 100% determinístico), e é o que roda
por padrão em um Codespace recém-criado, antes mesmo de configurar
qualquer segredo.

## Gerando uma chave do Gemini (gratuita)
1. Acesse https://aistudio.google.com/apikey;
2. Faça login com uma conta Google e clique em **Create API key**;
3. Copie a chave gerada e use como `GEMINI_API_KEY` (no Codespaces, como
   um *secret* do repositório; localmente, como variável de ambiente).
