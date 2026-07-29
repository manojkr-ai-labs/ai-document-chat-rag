from src.retriever.document_retriever import retrieve_documents
from src.prompts.rag_prompt import build_prompt
from src.agents.rag_agent import ask_llm
from src.services.citation_service import build_citations
from src.memory.conversation_memory import memory
from src.utils.logger import logger
from pathlib import Path

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

    # Ask LLM
    answer = ask_llm(prompt)

    # Save AI response
    memory.add_ai(answer)

    return {
        "answer": answer,
        "citations": citations,
    }