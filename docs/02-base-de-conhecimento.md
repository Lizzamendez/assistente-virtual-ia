# 2. Base de Conhecimento

## Onde está
`data/knowledge_base.json` — um arquivo JSON com 20 registros (chunks),
cada um representando um conceito de Administração de Empresas.

## Estrutura de cada registro
```json
{
  "id": "fin-ponto-equilibrio",
  "topic": "Gestão Financeira",
  "title": "Ponto de Equilíbrio",
  "content": "Texto explicativo do conceito, em linguagem clara...",
  "keywords": ["ponto de equilíbrio", "custos fixos", "break-even"]
}
```

- **id**: identificador único, usado nos testes e na avaliação.
- **topic**: categoria/área de conhecimento (facilita organização e
  relatórios).
- **title**: nome do conceito.
- **content**: explicação objetiva, escrita para ser lida por uma pessoa
  sem formação técnica em Administração.
- **keywords**: termos alternativos/sinônimos que ajudam a busca a
  encontrar o registro mesmo quando o usuário não usa exatamente o mesmo
  vocabulário do título.

## Áreas cobertas
| Área | Conceitos |
|---|---|
| Funções Administrativas | Planejamento, Organização, Direção, Controle |
| Gestão Financeira | Fluxo de Caixa, DRE, Ponto de Equilíbrio |
| Gestão de Pessoas | Recrutamento e Seleção, Motivação de Equipes |
| Marketing | 4 Ps, Segmentação de Mercado |
| Estratégia | SWOT, 5 Forças de Porter, Balanced Scorecard |
| Operações | Gestão de Processos, Gestão da Qualidade |
| Empreendedorismo | MVP, Plano de Negócios |
| Indicadores | KPIs, Produtividade e Eficiência |

## Como a base é usada
O módulo `src/kb.py` carrega esse JSON e cria um índice **TF-IDF**
(`TfidfVectorizer` do scikit-learn) sobre o texto de cada registro
(título + área + palavras-chave + conteúdo). Quando uma pergunta chega,
ela é comparada por **similaridade de cosseno** com todos os registros,
e os mais relevantes são retornados com uma pontuação de 0 a 1.

## Como evoluir a base
A base foi pensada para crescer de forma simples:
1. Adicione um novo objeto no array JSON, seguindo a mesma estrutura;
2. Escreva um `content` objetivo (2 a 4 frases) e algumas `keywords`
   relevantes;
3. Rode `python eval/evaluate.py` para conferir se a busca continua
   funcionando bem para as perguntas de teste.

Não é necessário re-treinar nada: o índice TF-IDF é reconstruído
automaticamente toda vez que o assistente é iniciado.
