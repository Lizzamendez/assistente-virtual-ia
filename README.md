# 🤖 AdminIA — Assistente Virtual de Administração de Empresas

Projeto do Lab **"Construa Seu Assistente Virtual Com Inteligência
Artificial"** (Digital Innovation One). O AdminIA é um assistente
conversacional que ajuda estudantes e pequenos empreendedores a entender
conceitos de **Administração de Empresas** (finanças, pessoas, marketing,
estratégia, operações, empreendedorismo e indicadores), respondendo com
base em uma base de conhecimento própria — sem inventar informações.

## ✨ O que ele faz
- Entende perguntas sobre gestão de empresas em linguagem natural;
- Busca as respostas em uma base de conhecimento organizada por área;
- Responde de forma clara e sugere um próximo passo prático;
- **Diz claramente quando não tem informação suficiente**, em vez de
  inventar uma resposta;
- Funciona 100% localmente (modo extrativo) ou, opcionalmente, com IA
  generativa (**Gemini**, do Google AI) para respostas mais fluidas.

## 🚀 Como rodar

### ☁️ Opção 1 — GitHub Codespaces (mais fácil, roda no navegador)
1. *(Opcional)* Cadastre `GEMINI_API_KEY` como *secret* do repositório em
   **Settings → Secrets and variables → Codespaces** (chave gratuita em
   https://aistudio.google.com/apikey). Sem ela, o assistente roda
   normalmente no modo extrativo local;
2. Clique em **Code → Codespaces → Create codespace on main** neste
   repositório;
3. Espere as dependências instalarem automaticamente e, no terminal,
   rode:
   ```bash
   cd src
   python cli.py
   ```

### 💻 Opção 2 — Localmente
```bash
git clone <este-repositorio>
cd assistente-virtual-ia
pip install -r requirements.txt

# (Opcional) habilitar respostas com IA generativa via Gemini
export GEMINI_API_KEY="sua-chave-aqui"

cd src
python cli.py
```

Sem a variável `GEMINI_API_KEY`, o assistente responde normalmente no
modo extrativo local (só com o texto da base de conhecimento) — nenhuma
funcionalidade fica bloqueada.

## 🧪 Como avaliar

```bash
python tests/test_assistant.py     # testes unitários rápidos
python eval/evaluate.py            # métricas de qualidade das respostas
```

O relatório de avaliação é salvo em `eval/report.md`.

## 📁 Estrutura do projeto

```
assistente-virtual-ia/
├── README.md
├── requirements.txt
├── .devcontainer/
│   └── devcontainer.json       # configuração do GitHub Codespaces
├── data/
│   └── knowledge_base.json     # base de conhecimento (20 tópicos de gestão)
├── docs/
│   ├── 01-documentacao.md      # o que o assistente faz e para quem
│   ├── 02-base-de-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-aplicacao.md
│   ├── 05-avaliacao.md
│   └── 06-pitch.md
├── src/
│   ├── kb.py                   # indexação e busca (TF-IDF)
│   ├── llm.py                  # geração de resposta (com/sem IA generativa)
│   ├── assistant.py            # classe principal do assistente
│   └── cli.py                  # interface de chat no terminal
├── eval/
│   ├── test_cases.json
│   ├── evaluate.py
│   └── report.md               # gerado automaticamente
└── tests/
    └── test_assistant.py
```

## 📚 Os 6 passos do desafio
Cada passo do desafio está documentado em detalhe na pasta `docs/`:

1. [Documentação](docs/01-documentacao.md)
2. [Base de Conhecimento](docs/02-base-de-conhecimento.md)
3. [Prompts](docs/03-prompts.md)
4. [Aplicação Funcional](docs/04-aplicacao.md)
5. [Avaliação e Métricas](docs/05-avaliacao.md)
6. [Pitch](docs/06-pitch.md)

## 🛠️ Tecnologias
- Python 3
- scikit-learn (TF-IDF + similaridade de cosseno) para busca na base de
  conhecimento
- Gemini API (Google AI) — opcional, para geração de respostas com IA
  generativa
- GitHub Codespaces / Dev Containers — ambiente de desenvolvimento pronto
  para uso, sem instalação local

## 📌 Baseado em
- [Repositório Base do desafio (DIO)](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro)
- [Repositório de exemplo — Edu, Educador Financeiro Inteligente](https://github.com/falvojr/dio-lab-bia-do-futuro)
