from src.llm_provider import llm
from src.utils.logger import logger


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