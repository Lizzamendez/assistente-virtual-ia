"""
Camada de geração de resposta em linguagem natural.

- Se a variável de ambiente GEMINI_API_KEY estiver definida e o pacote
  `google-generativeai` estiver instalado, o assistente usa o modelo
  Gemini (Google AI) para redigir uma resposta fluida, mas SEMPRE
  restrita ao contexto recuperado da base de conhecimento
  (RAG: Retrieval-Augmented Generation).
- Caso contrário, cai automaticamente em um modo extrativo/template, que
  monta a resposta apenas com o texto da base de conhecimento, sem
  inventar nada e sem depender de internet.

Isso garante que o projeto funcione "out of the box" mesmo sem chave de API.
"""
from __future__ import annotations

import os
from typing import List, Tuple

from kb import KBEntry

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """Você é o AdminIA, um assistente virtual especialista em Administração de Empresas.

Regras que você deve seguir SEMPRE:
1. Responda apenas com base no CONTEXTO fornecido abaixo. Nunca invente dados, números ou fatos que não estejam no contexto.
2. Se o contexto não for suficiente para responder com segurança, diga claramente que não tem informação suficiente e sugira ao usuário reformular a pergunta ou procurar um especialista humano.
3. Seja direto, claro e didático. Evite jargões sem explicá-los.
4. Sempre que fizer sentido, termine sugerindo um próximo passo prático para a pessoa usuária.
5. Responda sempre em português do Brasil.
"""


def _extractive_answer(question: str, contexts: List[Tuple[KBEntry, float]]) -> str:
    """Gera uma resposta apenas concatenando/organizando o conteúdo da base,
    sem usar nenhum modelo de linguagem externo."""
    if not contexts:
        return (
            "Não encontrei informação suficiente na minha base de conhecimento "
            "para responder a isso com segurança. Você pode reformular a pergunta "
            "ou me contar mais detalhes do seu contexto?"
        )

    top_entry, top_score = contexts[0]
    partes = [f"Sobre **{top_entry.title}** ({top_entry.topic}):", top_entry.content]

    extras = [c for c in contexts[1:] if c[1] >= 0.12]
    if extras:
        partes.append("\nTambém pode ser útil considerar:")
        for entry, _ in extras:
            partes.append(f"- **{entry.title}**: {entry.content}")

    partes.append(
        "\nPróximo passo sugerido: anote esse conceito e tente aplicá-lo a um "
        "exemplo real do seu negócio ou estudo de caso para fixar o aprendizado."
    )
    return "\n".join(partes)


def _try_gemini_answer(question: str, contexts: List[Tuple[KBEntry, float]]) -> str | None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai
    except ImportError:
        return None

    context_text = "\n\n".join(
        f"[{entry.title} - {entry.topic}] {entry.content}" for entry, _ in contexts
    ) or "(nenhum contexto relevante encontrado na base de conhecimento)"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
        response = model.generate_content(
            f"CONTEXTO RECUPERADO DA BASE DE CONHECIMENTO:\n{context_text}\n\n"
            f"PERGUNTA DO USUÁRIO:\n{question}",
            generation_config={"max_output_tokens": 500, "temperature": 0.3},
        )
        text = (getattr(response, "text", "") or "").strip()
        return text or None
    except Exception:
        # Qualquer erro de API (rede, chave inválida, cota excedida, etc.)
        # -> cai no modo extrativo, sem quebrar a aplicação.
        return None


def generate_answer(question: str, contexts: List[Tuple[KBEntry, float]]) -> str:
    """Ponto único de geração de resposta: tenta o modo com IA generativa
    (Gemini) e, se não for possível, usa o modo extrativo local."""
    answer = _try_gemini_answer(question, contexts)
    if answer:
        return answer
    return _extractive_answer(question, contexts)
