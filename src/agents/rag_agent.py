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
    """
    Stream tokens from the LLM.

    Args:
        prompt: Final prompt.

    Yields:
        Response chunks.
    """

    logger.info("=" * 60)
    logger.info("Streaming response from LLM...")
    logger.info("=" * 60)

    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content
