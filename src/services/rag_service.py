from src.retriever.reranked_retriever import RerankedRetriever
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm
from src.services.citation_service import build_citations
from src.memory.conversation_memory import memory
from src.utils.logger import logger


retriever = RerankedRetriever()


def answer_question(
    question: str,
    conversation: str | None = None,
):
    logger.info("=" * 60)
    logger.info("RAG request received")

    use_memory = conversation is None

    # Save user message
    if use_memory:
        memory.add_user(question)
        conversation = memory.get_context()

    # Retrieve documents
    results = retriever.retrieve(
        query=question,
    )

    documents = [
        result.document
        for result in results
    ]

    logger.info(
        f"Final relevant documents: {len(documents)}"
    )

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
    if use_memory:
        memory.add_ai(answer)

    return {
        "answer": answer,
        "citations": citations,
    }