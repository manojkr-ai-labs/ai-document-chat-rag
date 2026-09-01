from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.api.app import app
from src.api.routes import get_db


client = TestClient(app)


def override_get_db():
    yield Mock()


app.dependency_overrides[get_db] = override_get_db


def test_get_conversation_returns_404_when_missing():
    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.get_conversation_with_messages.return_value = None

        response = client.get(
            "/conversations/missing-conversation"
        )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Conversation not found"
def test_get_conversation_returns_conversation():
    conversation = {
        "id": "conversation-123",
        "title": "My Chat",
        "preview": "What is RAG?",
        "message_count": 2,
        "created_at": None,
        "updated_at": None,
        "messages": [
            {
                "id": "message-123",
                "role": "user",
                "content": "What is RAG?",
                "citations": None,
                "created_at": None,
            }
        ],
    }

    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.get_conversation_with_messages.return_value = conversation

        response = client.get(
            "/conversations/conversation-123"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Conversation retrieved successfully"
    assert data["data"]["id"] == "conversation-123"
    assert data["data"]["title"] == "My Chat"
    assert data["data"]["message_count"] == 2
    assert len(data["data"]["messages"]) == 1

def test_create_conversation():
    conversation = {
        "id": "conversation-123",
        "title": "My RAG Chat",
        "preview": None,
        "message_count": 0,
        "created_at": None,
        "updated_at": None,
    }

    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.create_conversation.return_value = conversation

        response = client.post(
            "/conversations",
            json={
                "title": "My RAG Chat",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Conversation created successfully"
    assert data["data"]["id"] == "conversation-123"
    assert data["data"]["title"] == "My RAG Chat"
    assert data["data"]["message_count"] == 0

    mock_service.return_value.create_conversation.assert_called_once_with(
        "My RAG Chat"
    )

def test_create_conversation_rejects_invalid_title():
    response = client.post(
        "/conversations",
        json={
            "title": 123,
        },
    )

    assert response.status_code == 422
def test_rename_conversation():
    conversation = {
        "id": "conversation-123",
        "title": "Renamed Chat",
        "preview": "What is RAG?",
        "message_count": 2,
        "created_at": None,
        "updated_at": None,
    }

    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.rename_conversation.return_value = conversation

        response = client.patch(
            "/conversations/conversation-123",
            json={
                "title": "Renamed Chat",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["id"] == "conversation-123"
    assert data["data"]["title"] == "Renamed Chat"

    mock_service.return_value.rename_conversation.assert_called_once_with(
        "conversation-123",
        "Renamed Chat",
    )
def test_rename_conversation_returns_404_when_missing():
    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.rename_conversation.return_value = None

        response = client.patch(
            "/conversations/missing-conversation",
            json={
                "title": "Renamed Chat",
            },
        )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Conversation not found"

    mock_service.return_value.rename_conversation.assert_called_once_with(
        "missing-conversation",
        "Renamed Chat",
    )
def test_delete_conversation():
    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.delete_conversation.return_value = True

        response = client.delete(
            "/conversations/conversation-123"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Conversation deleted successfully"

    mock_service.return_value.delete_conversation.assert_called_once_with(
        "conversation-123",
    )
def test_delete_conversation_returns_404_when_missing():
    with patch(
        "src.api.routes.ConversationService"
    ) as mock_service:

        mock_service.return_value.delete_conversation.return_value = False

        response = client.delete(
            "/conversations/missing-conversation"
        )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Conversation not found"

    mock_service.return_value.delete_conversation.assert_called_once_with(
        "missing-conversation",
    )
app.dependency_overrides.clear()
