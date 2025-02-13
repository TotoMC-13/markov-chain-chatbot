import nltk
import os
import asyncio
import random
from nltk.corpus import cess_esp
from markov_chain import MarkovChain
from db_handler import AsyncDatabaseConnection, DatabaseConnectionError

# Descarga de recursos NLTK necesarios (descomentar en la primera ejecución)
"""
nltk.download('cess_esp')  # Corpus en español
nltk.download('punkt')     # Tokenizador de oraciones
"""

# URL para la conexión a la base de datos
url = os.getenv("DB_URL")

async def main():
    try:
        database = AsyncDatabaseConnection(url)
        await database.connect(db_name="totobot", collection_name="transitions")
    except DatabaseConnectionError as e:
        print(f"Error de conexión a la base de datos: {e}")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return

    while True:
        try:
            print("1. Entrenar (crear cadena)")
            print("2. Borrar cadena")
            print("3. Generar texto")
            print("4. Salir")
            choice = int(input("Ingrese el número: "))
        except ValueError:
            print("Por favor, ingrese un número válido")
            continue
            
        try:
            if choice == 1:
                chain_length = int(input("Longitud de la cadena: "))
                while chain_length < 2:
                    print("La longitud de la cadena no puede ser menor a 2")
                    chain_length = int(input("Longitud de la cadena: "))

                # Usamos el corpus cess_esp que contiene textos en español
                text = cess_esp.sents()
                words = []

                for sentence in text:
                    for word in sentence:
                        words.append(word)

                markov = MarkovChain(n=chain_length)
                markov.create_transitions(words)

                prepared_data = markov.data_to_db()

                if not await database.insert(prepared_data):
                    print("No se pudo guardar la cadena")
                    
            elif choice == 2:
                if not await database.delete_all():
                    print("No se pudo borrar la cadena")
                    
            elif choice == 3:
                chain_length = int(input("Longitud de la cadena: "))
                while chain_length < 2:
                    print("La longitud de la cadena no puede ser menor a 2")
                    chain_length = int(input("Longitud de la cadena: "))
                
                markov = MarkovChain(n=chain_length)
                documents = await database.read_all()
                
                if not documents:
                    print("No hay datos en la base de datos")
                    continue
                
                try:
                    initial_chain = random.choice(documents)["context"]
                    generated_text = await markov.generate_text(database, initial_chain)
                    if generated_text:
                        print(" ".join(generated_text))
                    else:
                        print("No se pudo generar el texto")
                except Exception as e:
                    print(f"Error al generar texto: {e}")
                    
            elif choice == 4:
                await database.close()
                break
            else:
                print("Opción no válida")
                
        except Exception as e:
            print(f"Error en la operación: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error fatal: {e}")