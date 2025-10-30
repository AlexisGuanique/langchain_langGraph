from langchaing_core.messages import HumanMessage, AIMessage
from langchaing_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate([
   ("system", "Eres un experto en marketing, sugiere un slogan creativo para el siguiente producto: {producto}"),
   MessagesPlaceholder(variable_name="historial"),
   ("human", "{pregunta_actual}")
])

historial_conversacion = [
   HumanMessage(content="Hola, ¿cómo estás?"),
   AIMessage(content="Estoy bien, ¿y tú?"),
   HumanMessage(content="Estoy bien, gracias"),
]

mensajes = chat_prompt.invoke(
   historial=historial_conversacion,
   pregunta_actual="¿Cuál es el mejor producto para marketing?"
)

for mensaje in mensajes:
   print(f"Role: {mensaje.type}: {mensaje.content}")
