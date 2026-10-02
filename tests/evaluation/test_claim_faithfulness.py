from tests.evaluation.claim_faithfulness import (
    evaluate_claim_faithfulness,
)


def test_all_claims_are_supported():
    context = (
        "The examination has maximum marks of 100."
    )

    answer = (
        "The examination has maximum marks of 100."
    )

    score = evaluate_claim_faithfulness(
        answer=answer,
        context=context,
    )

    assert score == 1.0


def test_no_claims_are_supported():
    context = (
        "The examination has maximum marks of 100."
    )

    answer = (
        "The examination has maximum marks of 200."
    )

    score = evaluate_claim_faithfulness(
        answer=answer,
        context=context,
    )

    assert score == 0.0


def test_partial_claim_support():
    context = (
        "The examination has maximum marks of 100."
    )

    answer = (
        "The examination has maximum marks of 100 "
        "and lasts for 5 hours."
    )

    score = evaluate_claim_faithfulness(
        answer=answer,
        context=context,
    )

    assert 0.0 < score < 1.0


def test_empty_answer_returns_zero():
    score = evaluate_claim_faithfulness(
        answer="",
        context="The examination has maximum marks of 100.",
    )

    assert score == 0.0
def test_paraphrased_claim_is_supported():
    context = (
        "The 69th IATA Annual General Meeting "
        "addresses passenger rights and consumer "
        "protection."
    )

    answer = (
        "The IATA Annual General Meeting "
        "addresses passenger rights."
    )

    assert evaluate_claim_faithfulness(
        answer=answer,
        context=context,
    ) == 1.0


def test_claim_with_insufficient_overlap_is_unsupported():
    context = (
        "The examination is conducted for "
        "three hours."
    )

    answer = (
        "The examination is conducted "
        "in Mumbai."
    )

    assert evaluate_claim_faithfulness(
        answer=answer,
        context=context,
    ) == 0.0