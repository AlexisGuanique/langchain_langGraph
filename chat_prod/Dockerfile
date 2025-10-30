# Usar imagen base de Python oficial
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos de la aplicación
COPY chat_prompt_template.py .

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Variables de entorno para Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "chat_prompt_template.py", "--server.port=8501", "--server.address=0.0.0.0"]

