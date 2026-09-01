from unittest.mock import patch

from src.services.rag_stream_service import stream_answer


@patch("src.services.rag_stream_service.memory")
@patch("src.services.rag_stream_service.ask_llm_stream")
@patch("src.services.rag_stream_service.build_prompt")
@patch("src.services.rag_stream_service.build_citations")
@patch("src.services.rag_stream_service.retriever")
def test_stream_answer_uses_supplied_conversation(
    mock_retriever,
    mock_build_citations,
    mock_build_prompt,
    mock_ask_llm_stream,
    mock_memory,
):
    mock_retriever.retrieve.return_value = []

    mock_build_citations.return_value = [
        {
            "source": "/app/documents/example.pdf",
            "page": 0,
        }
    ]

    mock_build_prompt.return_value = "RAG PROMPT"

    mock_ask_llm_stream.return_value = iter(
        ["Hello", " from", " history"]
    )

    conversation = (
        "User: What did I ask before?\n"
        "AI: You asked about the project."
    )

    result = stream_answer(
        question="Can you remind me?",
        conversation=conversation,
    )

    chunks = list(result)

    assert chunks == [
        "Hello",
        " from",
        " history",
    ]

    mock_build_prompt.assert_called_once_with(
        context=[],
        question="Can you remind me?",
        conversation=conversation,
    )

    mock_memory.add_user.assert_not_called()
    mock_memory.add_ai.assert_not_called()