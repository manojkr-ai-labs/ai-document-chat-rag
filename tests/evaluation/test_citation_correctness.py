from tests.evaluation.citation_correctness import (
    evaluate_citation,
)


def test_citation_is_correct():
    cited_source = (
        "/app/documents/"
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf"
    )

    expected_sources = [
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
    ]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=expected_sources,
    ) is True


def test_citation_is_incorrect():
    cited_source = (
        "/app/documents/"
        "ietei-questions-papers.pdf"
    )

    expected_sources = [
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
    ]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=expected_sources,
    ) is False


def test_citation_accepts_multiple_expected_sources():
    cited_source = (
        "/app/documents/"
        "agm69-resolution-passenger-rights.pdf"
    )

    expected_sources = [
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        "agm69-resolution-passenger-rights.pdf",
    ]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=expected_sources,
    ) is True


def test_citation_rejects_unknown_source():
    cited_source = (
        "/app/documents/unknown.pdf"
    )

    expected_sources = [
        "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        "agm69-resolution-passenger-rights.pdf",
    ]

    assert evaluate_citation(
        cited_source=cited_source,
        expected_sources=expected_sources,
    ) is False