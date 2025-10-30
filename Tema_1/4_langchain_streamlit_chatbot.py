# Importamos las librerias necesarias

from langchain_openai import ChatOpenAI

# Ahora importamos las clases las cuales derivan de la clase BaseMessage, estas clases indican el rol del mensaje.
# AIMessage es el mensaje de la IA, HumanMessage es el mensaje del usuario, SystemMessage es el mensaje del sistema.
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Importamos PromptTemplate para crear templates estructurados
from langchain.prompts import PromptTemplate

# Libreria de python para crear interfaces de usuario.
import streamlit as st
# Librería para agregar retrasos en el streaming
import time

# Configuración de velocidad del streaming (delay entre chunks en segundos)
# Ajusta este valor para cambiar la velocidad: más alto = más lento, más bajo = más rápido
STREAMING_DELAY = 0.05  # Puedes cambiar este valor (0.0 = sin delay, 0.2 = muy lento)

# Configurar pagina de la app
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("Chatbot 🤖")
st.markdown(" Este es un chatbot creado con LangChain y Streamlit. Escribe algo para empezar a chatear.")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # Recrear el modelo con los nuevos parámetros
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)
    
    # Separador visual
    st.divider()
    
    # Botón para crear una nueva conversación
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        # Limpiar el historial de mensajes
        st.session_state.messages = []
        # Refrescar la página para limpiar la interfaz visualmente
        st.rerun()

# Crear el ChatPromptTemplate con las variables mensaje e historial
# Usamos ChatPromptTemplate para que sea compatible con ChatModel y LCEL
prompt_template = PromptTemplate(
   input_variables=["mensaje", "historial"],
   template="""Eres un asistente útil y amigable llamado ChatBot Pro. 

   Historial de conversación:
   {historial}

   Responde de manera clara y sencilla a la siguiente pregunta: {mensaje}"""
)

# st.session_state es un estado general que nos proporciona streamlit para guardar el estado de la app entre cada iteracion
# Inicializamos el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mstrar mensajes previos
for message in st.session_state.messages:
   if isinstance(message, SystemMessage):
      # No muestro el mensaje por pantalla
      continue
   # Especificamos el rol del mensaje que faltan
   role = "assistant" if isinstance(message, AIMessage) else "user"
   
   # Con esto le indicamos a streamlit que tipo de mensaje es y que lo muestre en la pantalla.
   with st.chat_message(role):
      st.markdown(message.content)
      

# Cuadro de entrada de texto para el usuario

pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
   # mostrar inmediato el mensaje del usuario en la interfaz
   with st.chat_message("user"):
      st.markdown(pregunta)
      
      # agregamos el mensaje al historial en la memoria de streamlit
      st.session_state.messages.append(HumanMessage(content=pregunta))
      
   # Formatear el historial de conversación como string para el template
   historial_str = ""
   for message in st.session_state.messages[:-1]:  # Excluir el último mensaje (la pregunta actual)
       if isinstance(message, HumanMessage):
           historial_str += f"Usuario: {message.content}\n"
       elif isinstance(message, AIMessage):
           historial_str += f"Asistente: {message.content}\n"
   
   # Si no hay historial previo, indicarlo
   if not historial_str:
       historial_str = "No hay conversación previa."
   
   # Usar LCEL (LangChain Expression Language) con el operador | para encadenar componentes
   # El operador | conecta el output del prompt_template directamente al input del chat_model
   cadena = prompt_template | chat_model
   
   # Implementar streaming de respuestas (mostrar la respuesta palabra por palabra)
   try:
       with st.chat_message("assistant"):
           # st.empty() crea un contenedor vacío que podemos actualizar dinámicamente
           response_placeholder = st.empty()
           # Variable para acumular la respuesta completa
           full_response = ""
           
           # Streaming: iteramos sobre cada "chunk" (fragmento) de respuesta que genera el modelo
           # cadena.stream() devuelve un generador que produce chunks de texto en tiempo real
           for chunk in cadena.stream({
               "mensaje": pregunta,
               "historial": historial_str
           }):
               # Acumulamos cada chunk en la respuesta completa
               full_response += chunk.content
               # Actualizamos el placeholder con la respuesta acumulada + cursor parpadeante "▌"
               # El cursor "▌" indica visualmente que la respuesta se está generando
               response_placeholder.markdown(full_response + "▌")
               # Agregar un pequeño delay para hacer el streaming más lento y visible
               time.sleep(STREAMING_DELAY)
           
           # Una vez terminado el streaming, actualizamos sin el cursor parpadeante
           response_placeholder.markdown(full_response)
       
       # Agregar la respuesta completa al historial después de que termine el streaming
       st.session_state.messages.append(AIMessage(content=full_response))
       
   except Exception as e:
       # Manejo de errores: capturamos cualquier excepción durante la generación
       st.error(f"Error al generar respuesta: {str(e)}")
       st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")