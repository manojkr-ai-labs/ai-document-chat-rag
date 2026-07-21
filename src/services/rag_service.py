from src.retriever.document_retriever import retrieve_documents
from src.agents.rag_agent import ask_llm


def ask_document(question: str):

    docs = retrieve_documents(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    answer = ask_llm(context, question)

    return answer