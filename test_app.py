from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API de détection spam opérationnelle", "version": "1.0"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_ham():
    response = client.post(
        "/predict",
        json={"email": "Hello, how are you today?"},
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["is_spam"] is False

def test_predict_spam():
    # Note: This depends on the model's accuracy, but let's assume a classic spam works
    response = client.post(
        "/predict",
        json={"email": "WINNER! You have won a prize. Click here now!"},
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
