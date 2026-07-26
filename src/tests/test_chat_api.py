def test_chat_success(client):
    response = client.post(
        "/chat",
        json={
            "question": "What is Docker?"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "answer" in body["data"]

def test_chat_empty_question(client):
    response = client.post(
        "/chat",
        json={
            "question": ""
        }
    )

    assert response.status_code in [200, 400, 422]   
def test_chat_missing_question(client):
    response = client.post(
        "/chat",
        json={}
    )

    assert response.status_code == 422

def test_chat_citations(client):
    response = client.post(
        "/chat",
        json={
            "question": "Docker"
        }
    )

    body = response.json()

    assert "citations" in body["data"]    