from typing import List
from langchain_core.documents import Document

SYSTEM_PROMPT = """
You are an AI assistant.

Answer ONLY from the provided context.

If the answer isn't available,
say you don't know.
"""
def build_prompt(
    context: List[Document],
    question: str
) -> str:
    """
    Build the final prompt for the LLM.

    Args:
        context: Retrieved document chunks.
        question: User question.

    Returns:
        Formatted prompt.
    """

    context_text = "\n\n".join(
        doc.page_content
        for doc in context
    )
    

    prompt = f"""
            {SYSTEM_PROMPT}

            =========================
            Context
            =========================

            {context_text}

            =========================
            Question
            =========================

            {question}

            =========================
            Answer
            =========================
            """

    return prompt