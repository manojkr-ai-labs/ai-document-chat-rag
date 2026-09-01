from types import SimpleNamespace
from unittest.mock import Mock

from src.services.conversation_service import ConversationService


def test_create_conversation():
    conversation = SimpleNamespace(
        id="conversation-123",
        title="My Chat",
        created_at=None,
        updated_at=None,
    )

    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.create = Mock(
        return_value=conversation
    )

    result = service.create_conversation("My Chat")

    service.conversation_repo.create.assert_called_once_with(
        "My Chat"
    )

    assert result["id"] == "conversation-123"
    assert result["title"] == "My Chat"
    assert result["preview"] is None
    assert result["message_count"] == 0
    assert "messages" not in result


def test_list_conversations_skips_empty_chats():
    empty_conversation = SimpleNamespace(
        id="empty-123",
        title="Empty Chat",
        created_at=None,
        updated_at=None,
    )

    conversation_with_message = SimpleNamespace(
        id="chat-123",
        title="My Chat",
        created_at=None,
        updated_at=None,
    )

    user_message = SimpleNamespace(
        role="user",
        content="What is RAG?",
    )

    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.list_all = Mock(
        return_value=[
            empty_conversation,
            conversation_with_message,
        ]
    )

    service.message_repo.list_by_conversation = Mock(
        side_effect=[
            [],
            [user_message],
        ]
    )

    result = service.list_conversations()

    assert len(result) == 1
    assert result[0]["id"] == "chat-123"
    assert result[0]["preview"] == "What is RAG?"
    assert result[0]["message_count"] == 1


def test_get_conversation_with_messages():
    conversation = SimpleNamespace(
        id="conversation-123",
        title="My Chat",
        created_at=None,
        updated_at=None,
    )

    user_message = SimpleNamespace(
        id="message-123",
        role="user",
        content="What is RAG?",
        citations=None,
        created_at=None,
    )

    assistant_message = SimpleNamespace(
        id="message-456",
        role="assistant",
        content="RAG retrieves relevant context before generating an answer.",
        citations=[
            {
                "source": "example.pdf",
                "page": "1",
            }
        ],
        created_at=None,
    )

    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=conversation
    )

    service.message_repo.list_by_conversation = Mock(
        return_value=[
            user_message,
            assistant_message,
        ]
    )

    result = service.get_conversation_with_messages(
        "conversation-123"
    )

    service.conversation_repo.get.assert_called_once_with(
        "conversation-123"
    )

    service.message_repo.list_by_conversation.assert_called_once_with(
        "conversation-123"
    )

    assert result["id"] == "conversation-123"
    assert result["title"] == "My Chat"
    assert result["preview"] == "What is RAG?"
    assert result["message_count"] == 2

    assert len(result["messages"]) == 2
    assert result["messages"][0]["role"] == "user"
    assert result["messages"][0]["content"] == "What is RAG?"
    assert result["messages"][1]["role"] == "assistant"
    assert result["messages"][1]["citations"] == [
        {
            "source": "example.pdf",
            "page": "1",
        }
    ]


def test_get_conversation_with_messages_returns_none_when_missing():
    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=None
    )

    service.message_repo.list_by_conversation = Mock()

    result = service.get_conversation_with_messages(
        "missing-conversation"
    )

    service.conversation_repo.get.assert_called_once_with(
        "missing-conversation"
    )

    service.message_repo.list_by_conversation.assert_not_called()

    assert result is None


def test_rename_conversation():
    conversation = SimpleNamespace(
        id="conversation-123",
        title="Old Title",
        created_at=None,
        updated_at=None,
    )

    renamed_conversation = SimpleNamespace(
        id="conversation-123",
        title="New Title",
        created_at=None,
        updated_at=None,
    )

    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=conversation
    )

    service.conversation_repo.rename = Mock(
        return_value=renamed_conversation
    )

    result = service.rename_conversation(
        "conversation-123",
        "New Title",
    )

    service.conversation_repo.get.assert_called_once_with(
        "conversation-123"
    )

    service.conversation_repo.rename.assert_called_once_with(
        conversation,
        "New Title",
    )

    assert result["id"] == "conversation-123"
    assert result["title"] == "New Title"
    assert result["preview"] is None
    assert result["message_count"] == 0


def test_rename_conversation_returns_none_when_missing():
    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=None
    )

    service.conversation_repo.rename = Mock()

    result = service.rename_conversation(
        "missing-conversation",
        "New Title",
    )

    service.conversation_repo.get.assert_called_once_with(
        "missing-conversation"
    )

    service.conversation_repo.rename.assert_not_called()

    assert result is None


def test_delete_conversation():
    conversation = SimpleNamespace(
        id="conversation-123",
        title="My Chat",
    )

    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=conversation
    )

    service.conversation_repo.delete = Mock()

    result = service.delete_conversation(
        "conversation-123"
    )

    service.conversation_repo.get.assert_called_once_with(
        "conversation-123"
    )

    service.conversation_repo.delete.assert_called_once_with(
        conversation
    )

    assert result is True


def test_delete_conversation_returns_false_when_missing():
    db = Mock()

    service = ConversationService(db)

    service.conversation_repo.get = Mock(
        return_value=None
    )

    service.conversation_repo.delete = Mock()

    result = service.delete_conversation(
        "missing-conversation"
    )

    service.conversation_repo.get.assert_called_once_with(
        "missing-conversation"
    )

    service.conversation_repo.delete.assert_not_called()

    assert result is False


def test_title_from_question_normalizes_whitespace():
    from src.services.conversation_service import title_from_question

    result = title_from_question(
        "   What   is   RAG?   "
    )

    assert result == "What is RAG?"


def test_title_from_question_returns_new_chat_for_empty_question():
    from src.services.conversation_service import title_from_question

    assert title_from_question("   ") == "New Chat"


def test_title_from_question_limits_length():
    from src.services.conversation_service import title_from_question

    question = "A" * 100

    result = title_from_question(question)

    assert len(result) == 60
    assert result.endswith("…")