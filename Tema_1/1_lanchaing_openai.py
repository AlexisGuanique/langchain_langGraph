# Nuestra primera app con Lang Chain
# Desde langchain_openai importamos la clase ChatOpenAI
from langchain_openai import ChatOpenAI
import os
# Recibe dos parametros:
# - model: el modelo de OpenAI a usar
# - temperature: el nivel de creatividad de la respuesta

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


pregunta = "¿En que año llegó el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta: ", respuesta.content)



