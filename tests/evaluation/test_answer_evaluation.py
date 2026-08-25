from tests.evaluation.answer_evaluation_questions import (
    ANSWER_EVALUATION_QUESTIONS,
)


def normalize_answer(answer: str) -> str:
    return " ".join(answer.lower().strip().split())


def test_answer_evaluation_dataset():

    assert ANSWER_EVALUATION_QUESTIONS

    for case in ANSWER_EVALUATION_QUESTIONS:

        assert case["question"]

        assert case["expected_answer"]

        assert case["expected_sources"]

        normalized = normalize_answer(
            case["expected_answer"]
        )

        assert normalized