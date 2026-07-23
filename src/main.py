from src.services.rag_service import answer_question
from src.utils.banner import show_banner


def main():

    show_banner()

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye!")
            break

        if not question:
            continue

        result = answer_question(question)

        print("\nAI:")
        print(result["answer"])

        print("\n📚 Sources")

        for citation in result["citations"]:
            print(
                f"- {citation['source']} (Page {citation['page']})"
            )


if __name__ == "__main__":
    main()