from unittest.mock import patch

from src.services.rag_service import answer_question
from tests.evaluation.answer_correctness import evaluate_answer


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_answer_is_correct(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    mock_retriever.retrieve.return_value = []

    mock_build_citations.return_value = []

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm.return_value = (
        "The BCS-011 examination carries a maximum of 100 marks."
    )

    result = answer_question(
        "What is the maximum marks for the BCS-011 examination?"
    )

    is_correct = evaluate_answer(
        generated_answer=result["answer"],
        expected_answer="100 marks.",
    )

    assert is_correct is True

    mock_ask_llm.assert_called_once_with(
        "RAG PROMPT"
    )


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_answer_is_incorrect(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    mock_retriever.retrieve.return_value = []

    mock_build_citations.return_value = []

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm.return_value = (
        "The BCS-011 examination lasts for 4 hours."
    )

    result = answer_question(
        "What is the time duration of the BCS-011 examination?"
    )

    is_correct = evaluate_answer(
        generated_answer=result["answer"],
        expected_answer="3 hours.",
    )

    assert is_correct is False