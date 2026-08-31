from pathlib import Path

from src.config.settings import EMBED_BATCH_SIZE
from src.utils.logger import logger
from src.utils.file_utils import get_pdf_files
from src.utils.hash_utils import calculate_file_hash
from src.services.index_manifest import (
    load_manifest,
    update_manifest,
    is_file_indexed,
)
from src.readers.document_loader import load_documents
from src.chunking.text_splitter import split_documents
from src.vectorstore.chroma_store import vector_db


def process_pdf(pdf_path, manifest):
    """
    Process one PDF and store it into ChromaDB.
    """

    logger.info(f"Checking: {pdf_path.name}")

    file_hash = calculate_file_hash(pdf_path)

    indexed = is_file_indexed(
        manifest,
        pdf_path.name,
        file_hash,
    )

    if indexed:
        logger.info("Already indexed")
        return False

    logger.info("Loading PDF...")
    documents = load_documents(pdf_path)

    logger.info(f"Loaded {len(documents)} pages")

    logger.info("Splitting into chunks...")
    chunks = split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    logger.info("Saving into ChromaDB...")

    total_batches = (
        len(chunks) + EMBED_BATCH_SIZE - 1
    ) // EMBED_BATCH_SIZE

    for i in range(0, len(chunks), EMBED_BATCH_SIZE):

        batch = chunks[i:i + EMBED_BATCH_SIZE]

        logger.info(
            "CHUNK %s | source=%s | page=%s | length=%s | preview=%s",
            i,
            chunks[i].metadata.get("source"),
            chunks[i].metadata.get("page"),
            len(chunks[i].page_content),
            chunks[i].page_content[:200].replace("\n", " "),
        )

        logger.info(
            f"Embedding batch "
            f"{i // EMBED_BATCH_SIZE + 1}/{total_batches}"
        )

        vector_db.add_documents(batch)

    update_manifest(
        manifest,
        pdf_path.name,
        file_hash,
    )

    logger.info("Indexed successfully")

    return True


def build_vector_database():
    """
    Build or update the vector database.
    """

    logger.info("=" * 60)
    logger.info("Building Vector Database")
    logger.info("=" * 60)

    manifest = load_manifest()

    pdf_files = get_pdf_files()

    indexed_count = 0
    skipped_count = 0

    for pdf in pdf_files:

        success = process_pdf(
            pdf,
            manifest,
        )

        if success:
            indexed_count += 1
        else:
            skipped_count += 1

    logger.info("")
    logger.info("=" * 60)
    logger.info("Indexing Complete")
    logger.info("=" * 60)

    logger.info(f"Indexed : {indexed_count}")
    logger.info(f"Skipped : {skipped_count}")
    logger.info(f"Total   : {len(pdf_files)}")


def index_single_document(pdf_path: str | Path) -> bool:
    """
    Index a single PDF without rebuilding the whole vector database.
    """

    pdf_path = Path(pdf_path)

    manifest = load_manifest()

    return process_pdf(
        pdf_path,
        manifest,
    )