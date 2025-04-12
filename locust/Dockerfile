FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de prueba
COPY locustfile.py .

# Exponer puertos para la interfaz web
EXPOSE 8089

# Comando para ejecutar Locust
ENTRYPOINT ["locust", "--host=http://postgres:5432"]