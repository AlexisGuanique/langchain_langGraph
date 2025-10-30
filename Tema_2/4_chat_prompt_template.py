# Cuando vamos a utilizar un prompt template, podemos hacerlo de dos maneras:

# 1. Usando el metodo format de la clase PromptTemplate.
# 2. Usando el metodo invoke de la clase ChatPromptTemplate.

# En este caso, vamos a usar el metodo invoke de la clase ChatPromptTemplate.
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate([
   ("system", "Eres una traductor al ingles de nivel superior, muy preciso"),
   ("human", "{texto}")
])

mesajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")

for m in mesajes:
   print(f"Role: {m.type}: {m.content}")

