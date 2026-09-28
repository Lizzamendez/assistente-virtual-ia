"""
Interface de linha de comando (CLI) do AdminIA.

Uso:
    python src/cli.py
"""
from assistant import AdminIAAssistant

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║   AdminIA - Assistente Virtual de Administração       ║
║   Digite sua dúvida sobre gestão de empresas.          ║
║   Digite 'sair' para encerrar.                         ║
╚══════════════════════════════════════════════════════╝
"""


def main():
    bot = AdminIAAssistant()
    print(BANNER)
    print(f"(Base de conhecimento carregada com {len(bot.kb)} tópicos)\n")

    while True:
        try:
            question = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if not question:
            continue
        if question.lower() in {"sair", "exit", "quit"}:
            print("AdminIA: Até logo! Bons negócios. 👋")
            break

        result = bot.ask(question)
        print(f"\nAdminIA: {result['answer']}")
        if result["used_topics"]:
            print(f"\n   [tópicos usados: {', '.join(result['used_topics'])} | confiança: {result['confidence']:.2f}]")
        else:
            print("\n   [nenhum tópico da base com confiança suficiente]")
        print()


if __name__ == "__main__":
    main()
