import PyPDF2
from io import BytesIO

# Declaramos nuestra funcion para extraer el texto de un archivo PDF.
def extraer_texto_pdf(archivo_pdf):
    try:
        # Leemos el archivo PDF.
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        # Inicializamos una variable para almacenar el texto completo.
        texto_completo = ""
        # Recorremos cada pagina del archivo PDF.
        # Enumerate es una funcion que nos permite recorrer el archivo PDF y obtener el numero de pagina.
        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            texto_pagina = pagina.extract_text()
            if texto_pagina.strip():
                texto_completo += f"\n--- PÁGINA {numero_pagina} ---\n"
                texto_completo += texto_pagina + "\n"
        # Eliminamos los espacios en blanco al principio y al final del texto.
        texto_completo = texto_completo.strip()
        # Si el texto esta vacio, retornamos un error.
        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."
        # Retornamos el texto completo.
        return texto_completo
    
    except Exception as e:
        # Si ocurre un error, retornamos un mensaje de error.
        return f"Error al procesar el archivo PDF: {str(e)}"