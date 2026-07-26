from pathlib import Path
def test_upload_without_file(client):
    response = client.post("/upload")

    assert response.status_code == 422

from pathlib import Path

def test_upload_pdf(client):
    pdf = Path("documents/LOLT Donation Form - Fillable.pdf")

    with open(pdf, "rb") as f:
        response = client.post(
            "/upload",
            files={
                "file": (
                    pdf.name,
                    f,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "processing"

def test_upload_returns_task_id(client):
    pdf = Path("documents/LOLT Donation Form - Fillable.pdf")

    with open(pdf, "rb") as f:
        response = client.post(
            "/upload",
            files={
                "file": (
                    pdf.name,
                    f,
                    "application/pdf",
                )
            },
        )

    body = response.json()

    assert body["data"]["task_id"]