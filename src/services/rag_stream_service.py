from src.retriever.document_retriever import retrieve_documents
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm_stream
from src.services.citation_service import build_citations
from src.memory.conversation_memory import memory
from src.utils.logger import logger


def stream_answer(question: str):
    """
    Stream an answer from the RAG pipeline.
    """

    logger.info("=" * 60)
    logger.info("Streaming Question Received")
    logger.info(question)

    # Save user message
    memory.add_user(question)

    # Retrieve documents
    documents = retrieve_documents(question)

    # Build prompt
    prompt = build_prompt(
        context=documents,
        question=question,
        conversation=memory.get_context(),
    )

    # Stream answer
    complete_answer = ""

    for chunk in ask_llm_stream(prompt):
        complete_answer += chunk
        yield chunk

    # Save final AI answer
    memory.add_ai(complete_answer)