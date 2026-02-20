# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application et les modèles
COPY . .

# Exposer le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
