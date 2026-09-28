"""
Módulo responsável por carregar e indexar a base de conhecimento
usando TF-IDF + similaridade de cosseno (busca semântica leve,
sem depender de nenhuma API externa).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class KBEntry:
    id: str
    topic: str
    title: str
    content: str
    keywords: List[str]

    def searchable_text(self) -> str:
        return f"{self.title}. {self.topic}. {' '.join(self.keywords)}. {self.content}"


class KnowledgeBase:
    """Carrega o JSON da base de conhecimento e permite buscas por similaridade."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.entries: List[KBEntry] = self._load(self.path)
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
        )
        self._matrix = self._vectorizer.fit_transform(
            [e.searchable_text() for e in self.entries]
        )

    @staticmethod
    def _load(path: Path) -> List[KBEntry]:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [KBEntry(**item) for item in raw]

    def search(self, query: str, top_k: int = 3):
        """Retorna até top_k entradas mais relevantes, cada uma com um score
        de similaridade entre 0 e 1 (quanto maior, mais relevante)."""
        query_vec = self._vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self._matrix)[0]
        ranked_idx = sims.argsort()[::-1][:top_k]
        results = [(self.entries[i], float(sims[i])) for i in ranked_idx]
        return results

    def get_by_id(self, entry_id: str) -> KBEntry | None:
        for e in self.entries:
            if e.id == entry_id:
                return e
        return None

    def __len__(self) -> int:
        return len(self.entries)
