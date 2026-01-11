FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# On installe streamlit explicitement ici pour être certain qu'il existe
RUN pip install --no-cache-dir streamlit pandas sqlalchemy psycopg2-binary plotly

COPY . .

EXPOSE 8501

# On utilise "python3 -m streamlit" qui est la méthode la plus sûre
CMD ["python3", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true"]