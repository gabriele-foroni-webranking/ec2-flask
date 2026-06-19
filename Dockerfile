FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Installa curl per healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copia i file delle dipendenze dalla cartella app
COPY app/requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice dalla cartella app
COPY app/ .

# Esponi la porta
EXPOSE 8000

# Avvia con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "60", "app:app"]