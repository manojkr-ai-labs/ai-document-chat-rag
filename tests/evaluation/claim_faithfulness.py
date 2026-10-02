import re

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "for",
    "from",
    "has",
    "have",
    "had",
    "he",
    "her",
    "his",
    "how",
    "i",
    "in",
    "is",
    "it",
    "its",
    "may",
    "might",
    "must",
    "of",
    "on",
    "or",
    "our",
    "should",
    "that",
    "the",
    "their",
    "them",
    "there",
    "these",
    "they",
    "this",
    "those",
    "to",
    "was",
    "were",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
}
def normalize_text(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s%.]",
        " ",
        text,
    )

    return " ".join(text.split())


def tokenize(text: str) -> set[str]:
    normalized = normalize_text(text)

    return {
        token
        for token in normalized.split()
        if token not in STOP_WORDS
    }


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

def claim_is_supported(
    claim: str,
    context: str,
) -> bool:
    """
    Determine whether a claim is supported
    by the retrieved context.

    Exact matching is preferred. For paraphrases,
    important factual values and entities must also
    be present in the context.
    """

    normalized_claim = normalize_text(claim)
    normalized_context = normalize_text(context)

    # 1. Exact match is strongest evidence.
    if normalized_claim in normalized_context:
        return True

    claim_tokens = tokenize(claim)
    context_tokens = tokenize(context)

    if not claim_tokens:
        return False

    # 2. Numeric values / percentages must be supported.
    claim_numbers = set(
        re.findall(
            r"\d+(?:\.\d+)?%?",
            claim,
        )
    )

    context_numbers = set(
        re.findall(
            r"\d+(?:\.\d+)?%?",
            context,
        )
    )

    if not claim_numbers.issubset(
        context_numbers
    ):
        return False

    # 3. Capitalized factual entities must be present.
    #
    # Example:
    #   Answer  -> Mumbai
    #   Context -> no Mumbai
    #
    # Therefore the claim is unsupported.
    claim_entities = {
        token
        for token in re.findall(
            r"\b[A-Z][A-Za-z0-9-]+\b",
            claim,
        )
        if token.lower() not in STOP_WORDS
    }

    context_entities = {
        token
        for token in re.findall(
            r"\b[A-Z][A-Za-z0-9-]+\b",
            context,
        )
        if token.lower() not in STOP_WORDS
    }

    if not claim_entities.issubset(
        context_entities
    ):
        return False

    # 4. Finally require sufficient meaningful
    # token overlap.
    claim_overlap = (
        claim_tokens & context_tokens
    )

    overlap = (
        len(claim_overlap)
        / len(claim_tokens)
    )

    return (
        overlap >= 0.60
        and len(claim_overlap) >= 2
    )
def evaluate_claim_faithfulness(
    answer: str,
    context: str,
) -> float:
    """
    Calculate the proportion of answer claims
    supported by the retrieved context.

    Returns:
        0.0 = no claims supported
        1.0 = all claims supported
    """

    claims = split_claims(answer)

    if not claims:
        return 0.0

    supported_claims = sum(
        claim_is_supported(
            claim,
            context,
        )
        for claim in claims
    )

    return (
        supported_claims
        / len(claims)
    )