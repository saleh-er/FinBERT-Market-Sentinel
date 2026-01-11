import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Récupération de l'URL depuis les variables d'environnement Docker
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle de la table Sentiment
class SentimentAnalysis(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String)
    headline = Column(String)
    label = Column(String)
    score = Column(Float)

# Création des tables
def init_db():
    Base.metadata.create_all(bind=engine)

def save_sentiment(ticker, headline, label, score):
    db = SessionLocal()
    new_entry = SentimentAnalysis(ticker=ticker, headline=headline, label=label, score=score)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()