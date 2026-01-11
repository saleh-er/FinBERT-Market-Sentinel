import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Market Sentiment Dashboard", layout="wide")

# Connexion à la DB (URL générée par Docker)
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

st.title("📈 Analyse de Sentiment Financier en Temps Réel")

try:
    # Lecture des données
    query = "SELECT * FROM sentiments ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)

    if not df.empty:
        # 1. KPI (Indicateurs clés)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Articles", len(df))
        col2.metric("Dernier Ticker", df['ticker'].iloc[0])
        col3.metric("Sentiment Dominant", df['label'].mode()[0])

        # 2. Graphique de répartition
        st.subheader("Répartition du Sentiment")
        fig = px.pie(df, names='label', color='label',
                     color_discrete_map={'Positive':'green', 'Neutral':'gray', 'Negative':'red'})
        st.plotly_chart(fig)

        # 3. Tableau de données
        st.subheader("Dernières Analyses")
        st.dataframe(df[['timestamp', 'ticker', 'headline', 'label', 'score']], use_container_width=True)
    else:
        st.info("En attente de données en provenance du collector...")

except Exception as e:
    st.error(f"Erreur de connexion à la base de données : {e}")

# Bouton de rafraîchissement manuel
if st.button('Actualiser les données'):
    st.rerun()