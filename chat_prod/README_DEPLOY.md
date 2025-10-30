# Guía de Despliegue del Chatbot en Google Cloud

## Prerrequisitos

1. Tener una cuenta de Google Cloud Platform (GCP)
2. Tener instalado Google Cloud SDK (gcloud)
3. Tener Docker instalado localmente (opcional, para probar antes)

## Opción 1: Desplegar en Compute Engine (VM)

### 1. Construir la imagen Docker

```bash
cd chat_prod
docker build -t chatbot-streamlit .
```

### 2. Subir la imagen a Google Container Registry (GCR)

```bash
# Autenticarse en GCP
gcloud auth login

# Configurar el proyecto
gcloud config set project TU_PROJECT_ID

# Habilitar Container Registry API
gcloud services enable containerregistry.googleapis.com

# Configurar Docker para usar gcloud
gcloud auth configure-docker

# Etiquetar la imagen
docker tag chatbot-streamlit gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest

# Subir la imagen
docker push gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest
```

### 3. Crear una VM en Compute Engine

```bash
# Crear una VM con Docker preinstalado
gcloud compute instances create chatbot-vm \
    --image-family=cos-stable \
    --image-project=cos-cloud \
    --machine-type=e2-medium \
    --zone=us-central1-a \
    --tags=http-server,https-server

# Abrir el puerto 8501 en el firewall
gcloud compute firewall-rules create allow-streamlit \
    --allow tcp:8501 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Streamlit port"
```

### 4. Conectar a la VM y ejecutar el contenedor

```bash
# Conectar por SSH
gcloud compute ssh chatbot-vm --zone=us-central1-a

# En la VM, ejecutar:
docker run -d \
    -p 8501:8501 \
    --name chatbot \
    gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest
```

### 5. Acceder al chatbot

Abre tu navegador en: `http://TU_IP_EXTERNA:8501`

Para obtener la IP externa:
```bash
gcloud compute instances describe chatbot-vm --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

## Opción 2: Desplegar en Cloud Run (Recomendado)

### 1. Construir y subir la imagen (igual que antes)

```bash
docker build -t chatbot-streamlit .
docker tag chatbot-streamlit gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest
docker push gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest
```

### 2. Desplegar en Cloud Run

```bash
gcloud run deploy chatbot-streamlit \
    --image gcr.io/TU_PROJECT_ID/chatbot-streamlit:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2
```

Cloud Run proporcionará automáticamente una URL HTTPS para tu aplicación.

## Configuración de API Key

La aplicación permite configurar la API Key desde la interfaz. Sin embargo, para producción puedes:

1. **Usar variables de entorno** (Recomendado):
   ```bash
   # En Cloud Run:
   gcloud run services update chatbot-streamlit \
       --set-env-vars OPENAI_API_KEY=tu_api_key_aqui
   
   # En Compute Engine (modificar Dockerfile):
   # Agregar: ENV OPENAI_API_KEY=tu_api_key_aqui
   ```

2. **Usar Secret Manager de GCP** (Más seguro):
   ```bash
   # Crear secreto
   echo -n "tu_api_key" | gcloud secrets create openai-api-key --data-file=-
   
   # En Cloud Run, dar acceso al secreto
   gcloud run services update chatbot-streamlit \
       --set-secrets OPENAI_API_KEY=openai-api-key:latest
   ```

## Verificación

1. Accede a la URL proporcionada
2. Ve al sidebar y configura tu API Key de OpenAI
3. Inicia una conversación para verificar que funciona

## Actualizar la aplicación

```bash
# Reconstruir y subir nueva versión
docker build -t chatbot-streamlit .
docker tag chatbot-streamlit gcr.io/TU_PROJECT_ID/chatbot-streamlit:v2
docker push gcr.io/TU_PROJECT_ID/chatbot-streamlit:v2

# Desplegar nueva versión (Cloud Run)
gcloud run deploy chatbot-streamlit \
    --image gcr.io/TU_PROJECT_ID/chatbot-streamlit:v2
```

## Notas importantes

- **Puerto**: El contenedor expone el puerto 8501
- **Memoria**: Se recomienda al menos 2GB de RAM
- **Costo**: Cloud Run cobra por uso, Compute Engine por tiempo de ejecución
- **Seguridad**: Considera usar HTTPS con un balanceador de carga o Cloud Run

