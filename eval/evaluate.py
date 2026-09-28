"""
Script de avaliação do AdminIA.

Mede:
- Hit@1: nas perguntas COM resposta esperada, o tópico correto foi o
  mais relevante recuperado?
- Hit@3: o tópico correto apareceu entre os 3 mais relevantes?
- Rejeição correta: nas perguntas fora do escopo (expected_id = null),
  o assistente disse corretamente que não tem informação suficiente?
- Confiança média nas perguntas dentro do escopo.

Gera um relatório em eval/report.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from assistant import AdminIAAssistant  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_PATH = BASE_DIR / "test_cases.json"
REPORT_PATH = BASE_DIR / "report.md"


def run_evaluation():
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    bot = AdminIAAssistant()

    in_scope = [c for c in cases if c["expected_id"] is not None]
    out_scope = [c for c in cases if c["expected_id"] is None]

    hit1 = 0
    hit3 = 0
    confidences = []
    rows = []

    for case in in_scope:
        contexts = bot._retrieve(case["question"], top_k=3)
        retrieved_ids = [e.id for e, _ in contexts]
        is_hit1 = len(retrieved_ids) > 0 and retrieved_ids[0] == case["expected_id"]
        is_hit3 = case["expected_id"] in retrieved_ids
        hit1 += int(is_hit1)
        hit3 += int(is_hit3)
        confidences.append(contexts[0][1] if contexts else 0.0)
        rows.append((case["question"], case["expected_id"], retrieved_ids, is_hit1, is_hit3))

    correct_rejections = 0
    rejection_rows = []
    for case in out_scope:
        result = bot.ask(case["question"])
        rejected = not result["had_enough_info"]
        correct_rejections += int(rejected)
        rejection_rows.append((case["question"], rejected))

    n_in = len(in_scope)
    n_out = len(out_scope)
    hit1_rate = hit1 / n_in if n_in else 0
    hit3_rate = hit3 / n_in if n_in else 0
    rejection_rate = correct_rejections / n_out if n_out else 0
    avg_conf = sum(confidences) / len(confidences) if confidences else 0

    report_lines = [
        "# Relatório de Avaliação - AdminIA",
        "",
        f"- Perguntas dentro do escopo avaliadas: {n_in}",
        f"- Perguntas fora do escopo avaliadas: {n_out}",
        f"- **Hit@1 (tópico correto em 1º lugar):** {hit1}/{n_in} = {hit1_rate:.0%}",
        f"- **Hit@3 (tópico correto entre os 3 primeiros):** {hit3}/{n_in} = {hit3_rate:.0%}",
        f"- **Confiança média nas perguntas dentro do escopo:** {avg_conf:.2f}",
        f"- **Taxa de rejeição correta (perguntas fora do escopo):** {correct_rejections}/{n_out} = {rejection_rate:.0%}",
        "",
        "## Detalhe - perguntas dentro do escopo",
        "",
        "| Pergunta | Esperado | Recuperado | Hit@1 | Hit@3 |",
        "|---|---|---|---|---|",
    ]
    for q, expected, retrieved, h1, h3 in rows:
        report_lines.append(f"| {q} | {expected} | {', '.join(retrieved)} | {'✅' if h1 else '❌'} | {'✅' if h3 else '❌'} |")

    report_lines += [
        "",
        "## Detalhe - perguntas fora do escopo (deveriam ser rejeitadas)",
        "",
        "| Pergunta | Rejeitou corretamente? |",
        "|---|---|",
    ]
    for q, rejected in rejection_rows:
        report_lines.append(f"| {q} | {'✅' if rejected else '❌'} |")

    report = "\n".join(report_lines) + "\n"
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\nRelatório salvo em: {REPORT_PATH}")


if __name__ == "__main__":
    run_evaluation()
