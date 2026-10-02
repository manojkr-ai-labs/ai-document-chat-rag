from unittest.mock import patch

 
@patch("src.services.chat_service.answer_question")
def test_chat_success(mock_answer, client):
    mock_answer.return_value = {
        "answer": "Docker is a container platform.",
        "citations": [],
    }

    response = client.post(
        "/chat",
        json={
            "question": "What is Docker?"
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Answer generated successfully"
    assert body["data"]["conversation_id"]
    assert body["data"]["answer"] == "Docker is a container platform."
    assert body["data"]["citations"] == []


 
@patch("src.services.chat_service.answer_question")
def test_chat_empty_question(mock_answer, client):
    mock_answer.return_value = {
        "answer": "",
        "citations": [],
    }

    response = client.post(
        "/chat",
        json={
            "question": "",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["answer"] == ""
    assert body["data"]["citations"] == []

def test_chat_missing_question(client):
    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422

 
@patch("src.services.chat_service.answer_question")
def test_chat_citations(mock_answer, client):
    mock_answer.return_value = {
        "answer": "Docker",
        "citations": [
            {
                "source": "docker.pdf",
                "page": 1,
            }
        ],
    }

    response = client.post(
        "/chat",
        json={
            "question": "Docker"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "citations" in body["data"]
    assert len(body["data"]["citations"]) == 1
    assert body["data"]["citations"][0]["source"] == "docker.pdf"