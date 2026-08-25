import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s%.]",
        " ",
        text,
    )

    return " ".join(text.split())


def split_claims(answer: str) -> list[str]:
    """
    Split an answer into simple factual claims.
    """
    claims = re.split(
        r"\s+(?:and|but|however)\s+|[.;]\s*",
        answer,
        flags=re.IGNORECASE,
    )

    return [
        claim.strip()
        for claim in claims
        if claim.strip()
    ]


def evaluate_claim_faithfulness(
    answer: str,
    context: str,
) -> float:
    """
    Calculate the proportion of answer claims
    directly supported by the context.

    Returns:
        0.0 = no claims supported
        1.0 = all claims supported
    """

    claims = split_claims(answer)

    if not claims:
        return 0.0

    normalized_context = normalize_text(context)

    supported_claims = 0

    for claim in claims:
        normalized_claim = normalize_text(claim)

        if normalized_claim in normalized_context:
            supported_claims += 1

    return supported_claims / len(claims)