from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_create_conversation():
    response = client.get("/conversations")
    assert response.status_code == 200
    assert "id" in response.json()


def test_list_conversations():
    response = client.get("/conversations")
    assert response.status_code == 200
    assert "id" in response.json()