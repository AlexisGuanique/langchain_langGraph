from langchain_core.prompts import PromptTemplate



# De esta manera definimos un prompt template con el metodo PromptTemplate de langchain.
# Aplicamos lo que se conoce como prompt engineering, es decir, estamos creando un prompt que se ajusta a la tarea que queremos que realice el modelo.
template = "Eres un experto en marketing, sugiere un slogan creativo para el siguiente producto: {producto}"


prompt = PromptTemplate(
   input_variables=["producto"],
   template=template
)

prompt_lleno = prompt.format(producto="Bebida energética")
print(prompt_lleno)


