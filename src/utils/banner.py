from pathlib import Path

from src.config import MODEL


def show_banner():
    """Display application startup banner."""

    docs_path = Path("documents")

    pdf_count = len(list(docs_path.glob("*.pdf")))

    print("=" * 60)
    print("🤖 AI Document Chat Assistant")
    print("=" * 60)
    print()
    print(f"Loaded Documents : {pdf_count}")
    print("Vector Database  : Ready")
    print(f"Model            : {MODEL}")
    print()
    print("Type 'exit' or 'quit' to quit.")
    print("-" * 60)