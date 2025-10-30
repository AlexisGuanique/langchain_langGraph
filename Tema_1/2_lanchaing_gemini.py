# Nuestra primera app con Lang Chain
# Desde langchain_google_genai importamos la clase ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Recibe dos parametros:
# - model: el modelo de Google Generative AI a usar
# - temperature: el nivel de creatividad de la respuesta

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)


pregunta = "¿En que año llegó el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta: ", respuesta.content)

