from unittest.mock import patch

from src.services.rag_service import answer_question
from tests.evaluation.citation_correctness import (
    evaluate_citation,
)


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_citation_is_correct(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    expected_source = (
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf"
    )

    mock_retriever.retrieve.return_value = []

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm.return_value = (
        "The BCS-011 examination carries a maximum "
        "of 100 marks."
    )

    mock_build_citations.return_value = [
        {
            "source": (
                "/app/documents/"
                "05._June_2012  BCS-011 "
                "IGNOUAssignmentGuru.com.pdf"
            ),
             "page": 0,
        }
    ]

    result = answer_question(
        "What is the maximum marks for the BCS-011 examination?"
    )

    citations = result["citations"]

    assert citations

    cited_source = citations[0]["source"]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=[expected_source],
    ) is True


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_citation_is_incorrect(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    expected_source = (
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf"
    )

    mock_retriever.retrieve.return_value = []

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm.return_value = (
        "The BCS-011 examination carries a maximum "
        "of 100 marks."
    )

    mock_build_citations.return_value = [
        {
            "source": (
                "/app/documents/"
                "ietei-questions-papers.pdf"
            ),
             "page": 0,
        }
    ]

    result = answer_question(
        "What is the maximum marks for the BCS-011 examination?"
    )

    citations = result["citations"]

    assert citations

    cited_source = citations[0]["source"]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=[expected_source],
    ) is False