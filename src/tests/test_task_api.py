def test_invalid_task(client):
    response = client.get("/tasks/invalid-id")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False

def test_invalid_task_message(client):
    response = client.get("/tasks/invalid-id")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["error"]["code"] == "TASK_NOT_FOUND"
    assert body["error"]["message"] == "Task not found"