from src.retriever.reranked_retriever import RerankedRetriever
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm_stream
from src.memory.conversation_memory import memory
from src.utils.logger import logger
from src.services.citation_service import build_citations


# Initialize once when the application starts/imports.
# The CrossEncoder model should NOT be loaded for every request.
retriever = RerankedRetriever()


def stream_answer(
    question: str,
    conversation: str | None = None,
):
    """
    Stream an answer from the RAG pipeline.
    """

    logger.info("=" * 60)
    logger.info("Streaming Question Received")
    logger.info(question)

    use_memory = conversation is None

    if use_memory:
        memory.add_user(question)
        conversation = memory.get_context()

    # Retrieve candidates → rerank → relevance gate
    documents = retriever.retrieve(
        query=question,
    )

    logger.info(
        f"Final relevant documents: {len(documents)}"
    )

    # Build citations from the same final documents
    citations = build_citations(
        [
            result.document
            for result in documents
        ]
    )

    logger.info(
        f"Generated {len(citations)} citations"
    )

    # Build RAG prompt
    prompt = build_prompt(
        context=[
            result.document
            for result in documents
        ],
        question=question,
        conversation=conversation,
    )

    logger.info("=" * 60)
    logger.info("FINAL RAG PROMPT")
    logger.info("=" * 60)
    logger.info(prompt)
    logger.info("=" * 60)

    complete_answer = ""

    for chunk in ask_llm_stream(prompt):
        complete_answer += chunk
        yield chunk

    if use_memory:
        memory.add_ai(complete_answer)

    return citations