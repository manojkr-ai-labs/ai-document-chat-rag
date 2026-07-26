def test_index(client):
    response = client.post("/index")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True