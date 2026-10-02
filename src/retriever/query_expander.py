import re


QUERY_EXPANSIONS = {
    "iata annual": "IATA Annual General Meeting",
    "iata general meeting": "IATA Annual General Meeting",
}


def expand_query(query: str) -> str:
    """
    Expand known short or incomplete queries
    into clearer domain-specific queries.

    If no expansion rule matches, return the
    original query unchanged.
    """

    normalized = re.sub(
        r"\s+",
        " ",
        query.strip().lower(),
    )

    for trigger, expanded in QUERY_EXPANSIONS.items():
        if trigger in normalized:
            return expanded

    return query