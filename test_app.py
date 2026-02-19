from fastapi.testclient import TestClient
from app import app
import warnings
from sklearn.exceptions import InconsistentVersionWarning
# Ignorer les avertissements de version de scikit-learn
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_ham():
    response = client.post("/predict", json={"email": "Bonjour !"})
    assert response.status_code == 200
    assert response.json()["is_spam"] is False
