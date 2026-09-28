# 6. Pitch — AdminIA

## O problema
Estudantes e pequenos empreendedores frequentemente precisam relembrar
rapidamente um conceito de gestão (o que é ponto de equilíbrio? o que é
uma análise SWOT?) no meio de uma tarefa real — montando uma planilha,
preparando uma reunião, respondendo uma prova. Pesquisar em vários sites
diferentes é lento, e nem sempre as fontes são claras ou confiáveis.

## A solução
O **AdminIA** é um assistente virtual conversacional especializado em
Administração de Empresas. Em vez de "conversar sobre qualquer coisa",
ele:
- Busca a resposta em uma **base de conhecimento curada** sobre gestão
  (finanças, pessoas, marketing, estratégia, operações, empreendedorismo
  e indicadores);
- Responde de forma **clara, direta e didática**;
- **Admite quando não sabe**, em vez de inventar uma resposta — algo
  essencial para gerar confiança em contexto de negócios;
- Sempre sugere um **próximo passo prático**, ajudando a pessoa a avançar
  na sua decisão, não só a "saber a matéria".

## Como funciona (por trás dos panos)
1. A pergunta do usuário é comparada com os tópicos da base de
   conhecimento usando busca por similaridade (TF-IDF);
2. Só os tópicos realmente relevantes (acima de um limiar de confiança)
   são usados como contexto;
3. Uma resposta é gerada — de forma opcionalmente potencializada por IA
   generativa (Gemini, via API do Google AI) sempre restrita a esse
   contexto, ou em modo extrativo local quando não há chave de API
   configurada — evitando "alucinações";
4. O histórico da conversa é mantido, permitindo perguntas de
   acompanhamento.

## Diferenciais
- **Funciona sem depender de API paga** (modo extrativo local), mas pode
  ser potencializado com IA generativa quando disponível;
- **Avaliação transparente**: métricas de precisão da busca (Hit@1/Hit@3)
  e da taxa de rejeição correta, com um relatório automático
  (`eval/report.md`) e falhas conhecidas documentadas honestamente;
- **Base de conhecimento fácil de expandir**, sem necessidade de
  re-treinar nenhum modelo.

## Próximos passos (roadmap)
- Trocar TF-IDF por embeddings semânticos para melhorar a precisão em
  perguntas com vocabulário diferente do da base;
- Adicionar uma interface web simples (ex.: Streamlit) além da CLI;
- Expandir a base de conhecimento com estudos de caso reais e
  calculadoras simples (ex.: calculadora de ponto de equilíbrio);
- Permitir que o usuário avalie cada resposta (👍/👎) para alimentar
  melhorias contínuas na base de conhecimento.

## Valor entregue
Um protótipo simples, funcional e honesto sobre suas próprias limitações
— exatamente o tipo de solução que demonstra domínio técnico (RAG,
avaliação, engenharia de prompt) e maturidade de produto (transparência,
foco no usuário) em um portfólio de Inteligência Artificial aplicada a
Administração de Empresas.
