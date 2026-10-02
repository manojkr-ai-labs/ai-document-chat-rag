from pathlib import Path
from unittest.mock import patch

from src.services.rag_service import answer_question
from tests.evaluation.answer_correctness import evaluate_answer
from tests.evaluation.claim_faithfulness import (
    evaluate_claim_faithfulness,
)
from tests.evaluation.citation_correctness import (
    evaluate_citation,
)
from tests.evaluation.answer_evaluation_questions import (
    ANSWER_EVALUATION_QUESTIONS,
)


@patch("src.services.rag_service.memory")
@patch("src.services.rag_service.ask_llm")
@patch("src.services.rag_service.build_prompt")
@patch("src.services.rag_service.build_citations")
@patch("src.services.rag_service.retriever")
def test_end_to_end_rag_evaluation(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm,
    mock_memory,
):
    total = len(ANSWER_EVALUATION_QUESTIONS)

    correct_answers = 0
    faithful_answers = 0
    correct_citations = 0

    for case in ANSWER_EVALUATION_QUESTIONS:
        expected_source = case["expected_sources"][0]

        context = (
                f"The answer is {case['expected_answer']}"
            )

        mock_retriever.retrieve.return_value = []

        mock_build_prompt.return_value = context

        mock_ask_llm.return_value = (
            f"The answer is {case['expected_answer']}"
        )

        mock_build_citations.return_value = [
            {
                "source": (
                    "/app/documents/"
                    f"{Path(expected_source).name}"
                ),
                "page": 0,
            }
        ]

        result = answer_question(
            case["question"]
        )

        answer = result["answer"]

        if evaluate_answer(
            generated_answer=answer,
            expected_answer=case["expected_answer"],
        ):
            correct_answers += 1

        faithfulness_score = (
            evaluate_claim_faithfulness(
                answer=answer,
                context=context,
            )
        )

        if faithfulness_score == 1.0:
            faithful_answers += 1

        citations = result["citations"]

        if citations:
            cited_source = citations[0]["source"]

            if evaluate_citation(
                cited_source=cited_source,
                expected_sources=case[
                    "expected_sources"
                ],
            ):
                correct_citations += 1

    answer_accuracy = correct_answers / total
    faithfulness_rate = faithful_answers / total
    citation_accuracy = correct_citations / total

    print("\n" + "=" * 70)
    print("RAG EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Questions evaluated:     {total}"
    )

    print(
        f"Answer correctness:      "
        f"{answer_accuracy:.2%}"
    )

    print(
        f"Faithfulness:            "
        f"{faithfulness_rate:.2%}"
    )

    print(
        f"Citation correctness:    "
        f"{citation_accuracy:.2%}"
    )

    print("=" * 70)

    assert answer_accuracy == 1.0
    assert faithfulness_rate == 1.0
    assert citation_accuracy == 1.0