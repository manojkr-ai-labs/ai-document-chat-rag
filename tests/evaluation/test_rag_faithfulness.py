from unittest.mock import patch

from src.services.rag_service import answer_question
from tests.evaluation.claim_faithfulness import (
    evaluate_claim_faithfulness,
)


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_answer_is_faithful(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    mock_retriever.retrieve.return_value = []

    mock_build_citations.return_value = []

    mock_build_prompt.return_value = context

    mock_ask_llm.return_value = (
        "The BCS-011 examination has maximum marks of 100."
    )

    result = answer_question(
        "What is the maximum marks for the BCS-011 examination?"
    )

    score = evaluate_claim_faithfulness(
        answer=result["answer"],
        context=context,
    )

    assert score == 1.0


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_rag_answer_contains_unsupported_claim(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    mock_retriever.retrieve.return_value = []

    mock_build_citations.return_value = []

    mock_build_prompt.return_value = context

    mock_ask_llm.return_value = (
        "The BCS-011 examination has maximum marks of 100 "
        "and lasts for 5 hours."
    )

    result = answer_question(
        "What is the maximum marks for the BCS-011 examination?"
    )

    score = evaluate_claim_faithfulness(
        answer=result["answer"],
        context=context,
    )

    assert 0.0 < score < 1.0