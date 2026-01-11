FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Installation forcée de la version sécurisée
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch>=2.6.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]