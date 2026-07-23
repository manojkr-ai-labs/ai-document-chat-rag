from src.retriever.document_retriever import retrieve_documents
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm
from src.services.citation_service import build_citations
from src.memory.conversation_memory import memory
from src.utils.logger import logger


def answer_question(question: str):

    logger.info("=" * 60)
    logger.info("Question Received")
    logger.info(question)

    # Save user message
    memory.add_user(question)

    # Conversation history
    conversation = memory.get_context()

    # Retrieve documents
    documents = retrieve_documents(question)

    # Build citations
    citations = build_citations(documents)

    # Build prompt
    prompt = build_prompt(
        context=documents,
        question=question,
        conversation=conversation,
    )

    # Ask LLM
    answer = ask_llm(prompt)

    # Save AI response
    memory.add_ai(answer)

    return {
        "answer": answer,
        "citations": citations,
    }