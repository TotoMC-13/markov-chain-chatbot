import nltk
import os
import asyncio
from nltk.corpus import cess_esp
from markov_chain import MarkovChain
from db_handler import AsyncDatabaseConnection  # Cambia la importación

# URL para la conexión a la base de datos
url = os.getenv("DB_URL")

async def main():
    database = AsyncDatabaseConnection(url)  # Ahora es asíncrono

    await database.connect(db_name="totobot", collection_name="transitions")

    # Descargar el corpus de nltk
    # nltk.download('cess_esp')
    # nltk.download('punkt')

    # Usamos el corpus cess_esp que contiene textos en español
    texto = cess_esp.sents()
    palabras = []

    for oracion in texto:
        for palabra in oracion:
            palabras.append(palabra)

    markov = MarkovChain()
    markov.create_transitions(palabras)

    prepared_data = markov.data_to_db()

    await database.insert(prepared_data)  # Ahora es await

    await database.close()  # Cerrar la conexión

# Ejecutar la función principal
asyncio.run(main())