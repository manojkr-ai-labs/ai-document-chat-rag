from tests.evaluation.faithfulness import evaluate_faithfulness


def test_faithful_answer():
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    answer = (
        "The BCS-011 examination has maximum marks of 100."
    )

    assert evaluate_faithfulness(
        answer=answer,
        context=context,
    ) is True


def test_unfaithful_answer():
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    answer = (
        "The BCS-011 examination has maximum marks of 200."
    )

    assert evaluate_faithfulness(
        answer=answer,
        context=context,
    ) is False


def test_faithful_answer_with_extra_whitespace():
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    answer = (
        "The BCS-011 examination has   maximum marks "
        "of 100."
    )

    assert evaluate_faithfulness(
        answer=answer,
        context=context,
    ) is True


def test_unfaithful_answer_with_extra_claim():
    context = (
        "The BCS-011 examination has maximum marks of 100."
    )

    answer = (
        "The BCS-011 examination has maximum marks of "
        "100 and lasts for 5 hours."
    )

    assert evaluate_faithfulness(
        answer=answer,
        context=context,
    ) is False