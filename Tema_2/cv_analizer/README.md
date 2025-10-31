# 📄 Sistema de Evaluación de CVs con IA

Sistema web para analizar currículums y evaluar candidatos de manera objetiva usando inteligencia artificial.

## 🚀 Despliegue con Docker

### Requisitos Previos

- Docker instalado
- API Key de OpenAI

### Pasos para Desplegar

1. **Construir la imagen Docker:**
```bash
docker build -t cv-analizer .
```

2. **Ejecutar el contenedor:**
```bash
docker run -d -p 8501:8501 -e OPENAI_API_KEY=tu_api_key_aqui --name cv-analizer --restart unless-stopped cv-analizer
```

3. **Acceder a la aplicación:**
   - Abre tu navegador en: `http://localhost:8501`
   - Si estás en un servidor remoto, usa: `http://tu_servidor_ip:8501`

### Comandos Útiles

**Ver logs del contenedor:**
```bash
docker logs cv-analizer
```

**Detener el contenedor:**
```bash
docker stop cv-analizer
```

**Eliminar el contenedor:**
```bash
docker rm cv-analizer
```

**Reconstruir y reiniciar:**
```bash
docker stop cv-analizer
docker rm cv-analizer
docker build -t cv-analizer .
docker run -d -p 8501:8501 -e OPENAI_API_KEY=tu_api_key_aqui --name cv-analizer --restart unless-stopped cv-analizer
```

## 📋 Estructura del Proyecto

```
cv_analizer/
├── app.py                 # Punto de entrada de la aplicación
├── ui/                    # Interfaz de usuario Streamlit
│   └── streamlit_ui.py
├── services/              # Servicios de negocio
│   ├── cv_evaluator.py   # Evaluación con IA
│   └── pdf_processor.py  # Procesamiento de PDFs
├── models/                # Modelos de datos
│   └── cv_model.py
├── prompts/               # Plantillas de prompts
│   └── cv_prompts.py
├── Dockerfile             # Configuración Docker
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

## 🔧 Configuración

La aplicación requiere la variable de entorno `OPENAI_API_KEY` para funcionar. Esta debe ser proporcionada al ejecutar el contenedor Docker.

## 📝 Notas

- La aplicación procesa archivos PDF con texto seleccionable
- Los PDFs escaneados (solo imágenes) pueden no funcionar correctamente
- Asegúrate de tener suficiente crédito en tu cuenta de OpenAI

