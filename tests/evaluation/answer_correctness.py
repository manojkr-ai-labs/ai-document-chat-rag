import re


def normalize_answer(answer: str) -> str:
    """
    Normalize an answer for comparison.
    """
    answer = answer.lower().strip()

    answer = re.sub(
        r"[^\w\s%.]",
        " ",
        answer,
    )

    return " ".join(answer.split())


def extract_numbers(text: str) -> list[str]:
    """
    Extract numeric values from text.

    Examples:
        '100 marks' -> ['100']
        '75%' -> ['75']
        '3 hours' -> ['3']
    """
    return re.findall(
        r"\d+(?:\.\d+)?",
        text,
    )


def evaluate_answer(
    generated_answer: str,
    expected_answer: str,
) -> bool:
    """
    Evaluate whether the expected answer
    is supported by the generated answer.
    """

    generated = normalize_answer(
        generated_answer
    )

    expected = normalize_answer(
        expected_answer
    )

    # Direct text match
    if expected in generated:
        return True

    # Numeric answer match
    expected_numbers = extract_numbers(
        expected
    )

    generated_numbers = extract_numbers(
        generated
    )

    if expected_numbers:
        return all(
            number in generated_numbers
            for number in expected_numbers
        )

    return False