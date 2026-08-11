from pathlib import Path
from src.utils.logger import logger

def build_citations(documents: list) -> list[dict]:
    """
    Build a unique list of source citations from retrieved documents.
    """

    citations = []
    seen = set()

    for doc in documents:
        source = Path(
            doc.metadata.get("source", "Unknown")
        ).name
        logger.info(
                f"Citation metadata: {doc.metadata}"
            )
        page = doc.metadata.get(
            "page_label",
            doc.metadata.get("page", "?")
        )

        key = (source, page)

        if key not in seen:
            seen.add(key)

            citations.append({
                "source": source,
                "page": page
            })

    return citations