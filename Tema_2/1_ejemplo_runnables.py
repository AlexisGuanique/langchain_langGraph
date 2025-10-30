#! Ejemplo de RunnableLambda
#! La clase RunnableLambda es una clase que nos invocar una funcion cualquiera creada por nosotros con el invoke de langchain.
from langchain_core.runnables import RunnableLambda

#? Ejemplo de una funcion lambda de python convertida en un RunnableLambda de langchain.
paso1 = RunnableLambda(lambda x: f"Numero: {x}")

#? Ejemplo de una funcion de python convertida en un RunnableLambda de langchain.
def duplicar_texto(texto):
   return [texto] * 2

paso2 = RunnableLambda(duplicar_texto)

#? Ahora creamos nuestra cadena de pasos.
cadena = paso1 | paso2

resultado = cadena.invoke(10)
print(resultado)