import time
from pathlib import Path

from src.services.rag_service import ask_document


DEFAULT_PDF = "data/NDSAP Implementation Guidelines 2.4.pdf"


def print_banner():
    print("=" * 70)
    print("🤖 AI DOCUMENT CHAT")
    print("=" * 70)
    print("Powered by:")
    print("• Ollama (llama3.2)")
    print("• nomic-embed-text")
    print("• LangChain")
    print("• ChromaDB")
    print("=" * 70)


def load_document():

    pdf_path = input(
        f"\nPDF Path (Press Enter for default)\n[{DEFAULT_PDF}]\n> "
    ).strip()

    if not pdf_path:
        pdf_path = DEFAULT_PDF

    if not Path(pdf_path).exists():
        raise FileNotFoundError(
            f"\n❌ PDF not found:\n{pdf_path}"
        )

    print("\n📄 Loading document...")
    print("⚡ Preparing AI system...")
    print("✅ Ready!\n")

    return pdf_path


def chat():

    print("\nType your question.")
    print("Type 'exit' or 'quit' to close.\n")

    while True:

        question = input("👤 You : ").strip()

        if not question:
            print("⚠️ Please enter a question.\n")
            continue

        if question.lower() in ["exit", "quit"]:

            print("\n👋 Thank you for using AI Document Chat.")
            break

        try:

            start = time.time()

            answer = ask_document(question)

            end = time.time()

            print("\n🤖 AI\n")
            print(answer)

            print(f"\n⏱ Response Time : {end-start:.2f} sec")

            print("-" * 70)

        except Exception as e:

            print(f"\n❌ Error : {e}")
            print("-" * 70)


def main():

    print_banner()

    try:

        load_document()

        chat()

    except KeyboardInterrupt:

        print("\n\nProgram Interrupted.")

    except Exception as e:

        print(f"\n❌ {e}")


if __name__ == "__main__":
    main()