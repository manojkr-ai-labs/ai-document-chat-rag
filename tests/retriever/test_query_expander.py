from src.retriever.query_expander import expand_query


def test_iata_annual_query_is_expanded():
    result = expand_query(
        "What is IATA Annual?"
    )

    assert result == (
        "IATA Annual General Meeting"
    )


def test_iata_general_meeting_query_is_expanded():
    result = expand_query(
        "IATA General Meeting"
    )

    assert result == (
        "IATA Annual General Meeting"
    )


def test_unrelated_query_is_unchanged():
    query = (
        "What is the maximum marks "
        "for the BCS-011 examination?"
    )

    result = expand_query(query)

    assert result == query