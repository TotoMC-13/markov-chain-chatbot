import nltk
import os
import asyncio
from nltk.corpus import cess_esp
from markov_chain import MarkovChain
from db_handler import AsyncDatabaseConnection

# URL para la conexión a la base de datos
url = os.getenv("DB_URL")

async def main():
    database = AsyncDatabaseConnection(url)  # Ahora es asíncrono

    await database.connect(db_name="totobot", collection_name="transitions")

    # Descargar el corpus de nltk
    # nltk.download('cess_esp')
    # nltk.download('punkt')

    while True:
        print("1. Entrenar (crear cadena)")
        print("2. Borrar cadena")
        print("3. Leer documentos")
        print("4. Salir")
        decision = int(input("Ingrese el numero: "))
        
        if decision == 1:
            long_cadena = int(input("Longitud de la cadena: "))
            while long_cadena < 2:
                print("La longitud de la cadena no puede ser menor a 2")
                long_cadena = int(input("Longitud de la cadena: "))

            # Usamos el corpus cess_esp que contiene textos en español
            texto = cess_esp.sents()
            palabras = []

            for oracion in texto:
                for palabra in oracion:
                    palabras.append(palabra)

            markov = MarkovChain(n=long_cadena)
            markov.create_transitions(palabras)

            prepared_data = markov.data_to_db()

            await database.insert(prepared_data)
        elif decision == 2:
            await database.delete_all()
        elif decision == 3:
            await database.read_all()
        elif decision == 4:
            await database.close()  # Cerrar la conexión
            quit()

# Ejecutar la función principal
asyncio.run(main())