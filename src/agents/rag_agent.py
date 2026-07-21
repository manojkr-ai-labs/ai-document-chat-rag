from src.llm_provider import llm
from src.prompts.rag_prompt import RAG_PROMPT


def ask_llm(context: str, question: str):

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.call(prompt)

    return response