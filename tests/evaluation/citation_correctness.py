from pathlib import Path


def normalize_source(source: str) -> str:
    """
    Normalize a source path to its filename.
    """
    return Path(source).name


def evaluate_citation(
    cited_source: str,
    expected_sources: list[str],
) -> bool:
    """
    Check whether the cited source is one of the
    expected sources.
    """

    normalized_citation = normalize_source(
        cited_source
    )

    normalized_expected_sources = {
        normalize_source(source)
        for source in expected_sources
    }

    return (
        normalized_citation
        in normalized_expected_sources
    )