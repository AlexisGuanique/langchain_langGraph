from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Preprocesa el texto: limpia espacios y limita a 500 caracteres
def preprocess_text(text):
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# Genera un resumen conciso del texto en una oración
def generar_resumen(text):
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content
 
resumen = RunnableLambda(generar_resumen)

# Analiza el sentimiento del texto y devuelve resultado en formato JSON
def analizar_sentimiento(text):
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        raise ValueError(f"Error al analizar el sentimiento: {response.content}")

sentimiento = RunnableLambda(analizar_sentimiento)


# Combina los resultados de resumen y análisis de sentimientos en un formato unificado
def unir_resultados(data):
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento"]["sentimiento"],
        "razon": data["sentimiento"]["razon"]
    }

merge = RunnableLambda(unir_resultados)


parallel_analisis = RunnableParallel({
   "resumen": resumen,
   "sentimiento": sentimiento
})

# Cadena completa

cadena = preprocessor | parallel_analisis | merge

# Pruebas del sistema
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde.",
    "Este producto es terrible, no funciona bien y es muy caro.",
    "Este producto es excelente, funciona perfectamente y es muy barato."
]
 
resultado_batch = cadena.batch(textos_prueba)

# Mostrar resultados de forma amigable
for i, (texto, resultado) in enumerate(zip(textos_prueba, resultado_batch), 1):
    print(f"\n{'='*70}")
    print(f"Análisis #{i}")
    print(f"{'='*70}")
    print(f"Texto original: {texto}")
    print(f"\nResumen: {resultado['resumen']}")
    print(f"Sentimiento: {resultado['sentimiento'].upper()}")
    print(f"Razón: {resultado['razon']}")
    print(f"{'='*70}")