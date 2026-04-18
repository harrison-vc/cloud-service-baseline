from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_data():
    response = client.get("/api/v1/data")
    assert response.status_code == 200
    assert "data" in response.json()
