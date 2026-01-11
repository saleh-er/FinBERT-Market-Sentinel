import time
import os
import requests
from database import init_db, save_sentiment
from transformers import pipeline

# Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  
TICKERS = ["NVIDIA", "TESLA", "BITCOIN", "APPLE"]

# Initialisation
init_db()
print("Base de données initialisée.")
print("Chargement de FinBERT...")
sentiment_model = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def fetch_real_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [a['title'] for a in articles]
    return []

def run_collector():
    for ticker in TICKERS:
        print(f"--- Recherche de news pour {ticker} ---")
        news_titles = fetch_real_news(ticker)
        
        for title in news_titles:
            # Analyse de sentiment
            result = sentiment_model(title)[0]
            label = result['label']
            score = result['score']
            
            # Sauvegarde
            save_sentiment(ticker, title, label, score)
            print(f"[{ticker}] Analysé: {label} ({score:.2f})")
        
        time.sleep(2) # Petite pause pour respecter les limites de l'API

if __name__ == "__main__":
    while True:
        try:
            run_collector()
        except Exception as e:
            print(f"Erreur : {e}")
        
        print("Cycle terminé. Prochaine mise à jour dans 15 minutes...")
        time.sleep(900) # L'API gratuite a des quotas, on espace les appels