from tests.evaluation.answer_correctness import evaluate_answer


def test_answer_correct_when_expected_text_is_present():
    result = evaluate_answer(
        generated_answer="The examination carries a maximum of 100 marks.",
        expected_answer="100 marks.",
    )

    assert result is True


def test_answer_incorrect_when_expected_text_is_missing():
    result = evaluate_answer(
        generated_answer="The examination lasts for 4 hours.",
        expected_answer="3 hours.",
    )

    assert result is False


def test_answer_correct_with_different_case():
    result = evaluate_answer(
        generated_answer="THE EXAMINATION HAS 100 MARKS.",
        expected_answer="100 marks.",
    )

    assert result is True


def test_answer_correct_with_extra_whitespace():
    result = evaluate_answer(
        generated_answer="The examination has   100   marks.",
        expected_answer="100 marks.",
    )

    assert result is True
def test_answer_correct_with_numeric_value_in_sentence():
    generated_answer = (
        "The maximum marks for the BCS-011 "
        "examination is 100."
    )

    expected_answer = "100 marks"

    assert evaluate_answer(
        generated_answer,
        expected_answer,
    ) is True