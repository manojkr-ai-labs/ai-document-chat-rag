from src.llm_provider import llm
from src.utils.logger import logger
from typing import Generator


def ask_llm(prompt: str) -> str:
    """
    Send prompt to the LLM and return the response.

    Args:
        prompt: Final prompt.

    Returns:
        AI response.
    """

    logger.info("=" * 60)
    logger.info("Sending prompt to LLM...")
    logger.info("=" * 60)

    response = llm.invoke(prompt)

    logger.info("LLM response received.")

    return response.content
def ask_llm_stream(prompt: str) -> Generator[str, None, None]:
    logger.info("=" * 60)
    logger.info("Streaming response from LLM...")
    logger.info("=" * 60)

    chunk_count = 0

    for chunk in llm.stream(prompt):
        chunk_count += 1

        logger.info(
            "LLM CHUNK %s: %r",
            chunk_count,
            chunk.content,
        )

        if chunk.content:
            yield chunk.content

    logger.info(
        "LLM STREAM COMPLETE. Total chunks: %s",
        chunk_count,
    )
