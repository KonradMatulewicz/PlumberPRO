from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok_and_version():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "version" in response.json()
