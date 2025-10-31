# Importamos el modelo de OpenAI.
from langchain_openai import ChatOpenAI
# Importamos el modelo de datos que esperamos que devuelva la IA.
from models.cv_model import AnalisisCV
# Importamos el prompt de sistema que usaremos para evaluar el CV.
from prompts.cv_prompts import crear_sistema_prompts
import os

# Declaramos nuestra funcion para crear el evaluador de CV.
def crear_evaluador_cv():
    # Obtenemos la API key desde variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está configurada. Por favor, configura la variable de entorno OPENAI_API_KEY.")
    
    # Creamos el modelo base de OpenAI.
    modelo_base = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion

# Declaramos nuestra funcion para evaluar el CV.
# Los parametros que le pasamos son el texto del CV y la descripcion del puesto.
# y nos devuelve el modelo de datos que esperamos que devuelva la IA.
def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        return resultado
    
    except Exception as e:
        # retornamos un objeto de tipo AnalisisCV de pydantic con los datos de error.
        return AnalisisCV(
            nombre_candidato="Error en procesamiento.",
            experiencia_años=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar.",
            experiencia_relevante="Error durante el análisis.",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0
        )
