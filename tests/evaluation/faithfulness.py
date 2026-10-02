import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s%.]",
        " ",
        text,
    )

    return " ".join(text.split())


def evaluate_faithfulness(
    answer: str,
    context: str,
) -> bool:
    """
    Check whether the important factual content
    in the answer is supported by the context.
    """

    normalized_answer = normalize_text(answer)
    normalized_context = normalize_text(context)

    return normalized_answer in normalized_context