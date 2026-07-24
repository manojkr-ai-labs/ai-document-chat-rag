from pathlib import Path


DOCUMENTS_DIR = Path("documents")


def save_document(file_name: str, content: bytes) -> str:
    """
    Save uploaded PDF into documents directory.
    """

    DOCUMENTS_DIR.mkdir(exist_ok=True)

    file_path = DOCUMENTS_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)