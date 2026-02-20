from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import joblib
from sklearn.feature_extraction.text import CountVectorizer
import os

app = FastAPI()

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    email: str

# Charger les modèles (avec gestion d'erreurs)
try:
    cv = joblib.load("count_vectorizer.pkl")
    model = joblib.load("dtcspam_model.pkl")
    print("✅ Modèles chargés avec succès!")
except Exception as e:
    print(f"❌ Erreur chargement modèles: {e}")
    # En production, vous voudrez peut-être arrêter l'application
    raise e

@app.get("/")
def working():
    return FileResponse("index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        email = input_data.email
        print(f"📧 Message reçu: {email[:100]}...")  # Log partiel
        
        # Transformation du texte
        email_count = cv.transform([email])
        
        # Prédiction
        prediction = model.predict(email_count)
        prediction_int = int(prediction[0])
        
        result = {
            "prediction": prediction_int,
            "is_spam": bool(prediction_int),
            "message_length": len(email)
        }
        
        print(f"🔮 Prédiction: {'SPAM' if prediction_int else 'NON-SPAM'}")
        return result
        
    except Exception as e:
        print(f"❌ Erreur prédiction: {e}")
        return {"error": str(e), "prediction": 0}