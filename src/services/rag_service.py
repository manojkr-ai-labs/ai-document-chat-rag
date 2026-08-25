from src.retriever.reranked_retriever import RerankedRetriever
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm
from src.services.citation_service import build_citations
from src.memory.conversation_memory import memory
from src.utils.logger import logger
from pathlib import Path
from unittest.mock import patch

retriever = RerankedRetriever()

def answer_question(question: str):

    logger.info("=" * 60)
    logger.info("Question Received")
    logger.info(question)

    # Save user message
    memory.add_user(question)

    # Conversation history
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
    citationsResult = build_citations(documents)
    unique = {}
    normalized_citations = []
    for citation in citationsResult:
      file_name = Path(citation["source"]).name
      page = str(citation["page"])
      key = f"{file_name}-{page}"
      if key not in unique:
            unique[key] = True
            normalized_citations.append({
                "source": file_name,
                "page": page,
        })  
    citations = normalized_citations
    # Build prompt
    prompt = build_prompt(
        context=documents,
        question=question,
        conversation=conversation,
    )
    real_retriever = answer_question.__globals__["retriever"]

    captured_results = []

    original_retrieve = real_retriever.retrieve


    def capture_retrieve(*args, **kwargs):
        results = original_retrieve(*args, **kwargs)
        captured_results.extend(results)
        return results

    # Ask LLM
    answer = ask_llm(prompt)

    # Save AI response
    memory.add_ai(answer)

    return {
        "answer": answer,
        "citations": citations,
    }