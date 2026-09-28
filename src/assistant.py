"""
AdminIA - Assistente Virtual de Administração de Empresas

Junta:
- Recuperação de informação (kb.py) na base de conhecimento;
- Geração de resposta (llm.py), com ou sem IA generativa;
- Memória simples da conversa (histórico);
- Regra explícita de "não sei" quando a confiança da busca é baixa.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from kb import KnowledgeBase, KBEntry
from llm import generate_answer

# Abaixo desse score de similaridade, consideramos que a base de
# conhecimento não tem informação suficiente sobre o assunto.
CONFIDENCE_THRESHOLD = 0.12

DEFAULT_KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"


class AdminIAAssistant:
    def __init__(self, kb_path: str | Path = DEFAULT_KB_PATH):
        self.kb = KnowledgeBase(kb_path)
        self.history: List[dict] = []  # [{"role": "user"/"assistant", "content": str}]

    def _retrieve(self, question: str, top_k: int = 3) -> List[Tuple[KBEntry, float]]:
        results = self.kb.search(question, top_k=top_k)
        # Filtra apenas o que passa do limiar de confiança
        return [(entry, score) for entry, score in results if score >= CONFIDENCE_THRESHOLD]

    def ask(self, question: str) -> dict:
        """Processa uma pergunta e retorna um dicionário com a resposta e
        metadados úteis para depuração/avaliação."""
        question = question.strip()
        self.history.append({"role": "user", "content": question})

        contexts = self._retrieve(question)
        answer = generate_answer(question, contexts)

        self.history.append({"role": "assistant", "content": answer})

        return {
            "question": question,
            "answer": answer,
            "used_topics": [entry.title for entry, _ in contexts],
            "confidence": contexts[0][1] if contexts else 0.0,
            "had_enough_info": bool(contexts),
        }

    def reset(self):
        self.history = []


if __name__ == "__main__":
    bot = AdminIAAssistant()
    print(f"Base de conhecimento carregada com {len(bot.kb)} tópicos.\n")
    resp = bot.ask("O que é ponto de equilíbrio?")
    print(resp["answer"])
