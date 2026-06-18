FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file delle dipendenze dalla cartella app
COPY app/requirements.txt .

# Installa le dipendenze
RUN pip install -r requirements.txt

# Copia tutto il codice dalla cartella app
COPY app/ .

# Esponi la porta
EXPOSE 8000

# Avvia con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]