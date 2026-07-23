from src.retriever.document_retriever import retrieve_documents
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm
from src.services.citation_service import build_citations
from src.utils.logger import logger


def answer_question(question: str) -> str:
    logger.info("=" * 60)
    logger.info("Question Received")
    logger.info(question)

    documents = retrieve_documents(question)
    citations = build_citations(documents)  

    prompt = build_prompt(
        context=documents,
        question=question, 
    )

    answer = ask_llm(prompt)

    return {
    "answer": answer,
    "citations": citations
    }