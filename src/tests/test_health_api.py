def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["healthy"] is True

def test_health_contains_checks(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    checks = body["data"]["checks"]

    assert "ollama" in checks
    assert "chroma" in checks
    assert "disk" in checks