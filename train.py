import nltk
import os
import asyncio
import random
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
        print("3. Generar texto")
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
            long_cadena = int(input("Longitud de la cadena: "))
            while long_cadena < 2:
                print("La longitud de la cadena no puede ser menor a 2")
                long_cadena = int(input("Longitud de la cadena: "))
            
            markov = MarkovChain(n=long_cadena)
            documents = await database.read_all()
            
            if not documents:
                print("No hay datos en la base de datos")
                continue
            
            initial_chain = random.choice(documents)["context"]
            generated_text = await markov.generate_text(database, initial_chain)
            
            print(" ".join(generated_text))

        elif decision == 4:
            await database.close()  # Cerrar la conexión
            quit()

# Ejecutar la función principal
asyncio.run(main())