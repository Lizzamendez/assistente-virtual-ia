"""
Testes unitários simples do AdminIA (sem dependências externas de teste,
para manter o projeto leve — pode ser rodado com `python -m pytest` se
o pytest estiver instalado, ou diretamente com `python tests/test_assistant.py`).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from assistant import AdminIAAssistant  # noqa: E402


def test_kb_carrega_entradas():
    bot = AdminIAAssistant()
    assert len(bot.kb) > 0, "A base de conhecimento não pode estar vazia"


def test_pergunta_dentro_do_escopo_retorna_topico():
    bot = AdminIAAssistant()
    result = bot.ask("O que é análise SWOT?")
    assert result["had_enough_info"] is True
    assert "SWOT" in result["used_topics"][0] or "Swot" in result["used_topics"][0]


def test_pergunta_fora_do_escopo_admite_nao_saber():
    bot = AdminIAAssistant()
    result = bot.ask("Quem foi o pintor Pablo Picasso?")
    assert result["had_enough_info"] is False
    assert "não" in result["answer"].lower() or "reformular" in result["answer"].lower()


def test_historico_registra_conversa():
    bot = AdminIAAssistant()
    bot.ask("O que é fluxo de caixa?")
    assert len(bot.history) == 2  # 1 pergunta + 1 resposta
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def _run_all():
    testes = [
        test_kb_carrega_entradas,
        test_pergunta_dentro_do_escopo_retorna_topico,
        test_pergunta_fora_do_escopo_admite_nao_saber,
        test_historico_registra_conversa,
    ]
    falhas = 0
    for teste in testes:
        try:
            teste()
            print(f"OK   - {teste.__name__}")
        except AssertionError as e:
            falhas += 1
            print(f"FALHOU - {teste.__name__}: {e}")
    print(f"\n{len(testes) - falhas}/{len(testes)} testes passaram.")


if __name__ == "__main__":
    _run_all()
