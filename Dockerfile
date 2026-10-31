# 1. Utilizar una imagen oficial y ligera de Python
FROM python:3.10-slim

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalar herramientas del sistema necesarias para dependencias científicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiar e instalar las dependencias de Python primero (optimización de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código fuente y modelos del proyecto
COPY . /app

# 6. Exponer el puerto en el que correrá la API
EXPOSE 8000

# 7. Comando predeterminado para iniciar la aplicación mediante Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]