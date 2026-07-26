from unittest.mock import patch


@patch("src.api.routes.index_documents")
def test_index(mock_index, client):
    mock_index.return_value = None

    response = client.post("/index")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Documents indexed successfully"