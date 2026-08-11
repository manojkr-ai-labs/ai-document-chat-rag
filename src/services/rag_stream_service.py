from src.retriever.document_retriever import retrieve_documents
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm_stream
from src.memory.conversation_memory import memory
from src.utils.logger import logger
from src.services.citation_service import build_citations


def stream_answer(question: str):
    """
    Stream an answer from the RAG pipeline.
    """

    logger.info("=" * 60)
    logger.info("Streaming Question Received")
    logger.info(question)

    memory.add_user(question)

    # Retrieve relevant documents
    documents = retrieve_documents(question)

    # Build citations from the same retrieved documents
    citations = build_citations(documents)

    logger.info(
        f"Generated {len(citations)} citations"
    )

    # Build RAG prompt
    prompt = build_prompt(
        context=documents,
        question=question,
        conversation=memory.get_context(),
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

    memory.add_ai(complete_answer)

    return citations