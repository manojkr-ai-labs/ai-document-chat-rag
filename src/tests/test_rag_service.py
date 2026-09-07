from unittest.mock import patch

from langchain_core.documents import Document

from src.services.rag_service import answer_question


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_answer_question_returns_answer_and_citations(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    document = Document(
        page_content="Docker is a container platform.",
        metadata={
            "source": "/app/documents/docker.pdf",
            "page": 1,
        },
    )

    mock_result = type(
        "RetrievalResult",
        (),
        {"document": document},
    )()

    mock_retriever.retrieve.return_value = [mock_result]

    mock_build_citations.return_value = [
        {
            "source": "docker.pdf",
            "page": "1",
        }
    ]

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm.return_value = (
        "Docker is a container platform."
    )

    result = answer_question("What is Docker?")

    assert result["answer"] == (
        "Docker is a container platform."
    )

    assert result["citations"] == [
        {
            "source": "docker.pdf",
            "page": "1",
        }
    ]

    mock_retriever.retrieve.assert_called_once_with(
        query="What is Docker?",
    )

    mock_build_citations.assert_called_once_with(
        [document]
    )

    mock_build_prompt.assert_called_once()

    mock_ask_llm.assert_called_once_with(
        "RAG PROMPT"
    )


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_answer_question_returns_citations_from_citation_service(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    document = Document(
        page_content="Docker information.",
        metadata={
            "source": "/app/documents/docker.pdf",
            "page": 1,
        },
    )

    mock_result = type(
        "RetrievalResult",
        (),
        {"document": document},
    )()

    mock_retriever.retrieve.return_value = [
        mock_result,
        mock_result,
    ]

    citations = [
        {
            "source": "docker.pdf",
            "page": "1",
        }
    ]

    mock_build_citations.return_value = citations

    mock_build_prompt.return_value = "RAG PROMPT"
    mock_ask_llm.return_value = "Docker answer."

    result = answer_question("What is Docker?")

    assert result["answer"] == "Docker answer."

    assert result["citations"] == citations

    mock_build_citations.assert_called_once_with(
        [document, document]
    )