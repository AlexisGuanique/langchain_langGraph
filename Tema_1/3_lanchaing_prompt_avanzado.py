# Nuestra primera app con Lang Chain
# Desde langchain_openai importamos la clase ChatOpenAI
from langchain_openai import ChatOpenAI
# Desde langchaing.promts importamos la clase PromptTemplate para crear prompts avanzados
from langchain.prompts import PromptTemplate
# Desde langchain.chains importamos la clase LLMChain para crear cadenas LLM
# Sin embargo este mecanismo esta deprecado
# from langchain.chains import LLMChain


chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Creamos nuestro prompt avanzado en forma de plantilla.
# A esta plantilla le podemos pasar varias variables como por ejemplo:
# input_variables: las variables que le pasaremos a la plantilla
# template: el prompt indicando donde debe colocar la variable
plantilla = PromptTemplate(
   input_variables=["nombre"],   
   template="Saluda al usuario con su nombre. \nNombre del usuario: {nombre} \nAsistente: "
)

# Las cadenas son de mucha importancia en LangChain, son una frecuencia de pasos que nos permite invocar un llm con un prompt avanzado.


#! Estas pueden ser secuenciales, es decir que va ejecutando cada paso de la cadena.
# Tambien pueden haber grafos con LangGraph

# Definimos la cadena indicando cada paso de la cadena uno por uno.
# En este caso indicamos dos pasos:
# 1. Indicamos el LLM a usar
# 2. Indicamos el prompt avanzado a usar
# chain = LLMChain(llm=chat, prompt=plantilla)

# # luego con el metodo run de chain corremos la cadena, pasandole las variables necesarias.
# resultado = chain.run(nombre="Alexis")


#! Ahora esta es la manera de hacerlo con el nuevo mecanismo de Sequential Chain

chain = plantilla | chat

resultado = chain.invoke({"nombre": "Alexis"})

print(resultado.content)

