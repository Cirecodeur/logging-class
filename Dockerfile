# Utilise une image Python légère
FROM python:3.11-slim

# Définit le dossier de travail À L'INTÉRIEUR de Docker (ne change rien chez toi)
WORKDIR /app

# Copie TOUS tes fichiers locaux vers le dossier /app de Docker
COPY . .

# Installe les bibliothèques listées dans ton requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port par défaut de Streamlit
EXPOSE 8501

# Commande pour lancer l'application au démarrage du container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]