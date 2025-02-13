import nltk
import os
import asyncio
import random
from nltk.corpus import cess_esp
from markov_chain import MarkovChain
from db_handler import AsyncDatabaseConnection, DatabaseConnectionError

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_text_result(text):
    """Muestra el texto generado con formato mejorado"""
    clear_screen()
    print("\n" + "="*50)
    print("\nTEXTO GENERADO:")
    print("-"*50)
    print(" ".join(text))
    print("\n" + "="*50)
    input("\nPresione Enter para continuar...")
    clear_screen()

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
        clear_screen()
        print("Generador de texto con cadenas de Markov")
        print("="*50 + "\n")
        print("1. Entrenar (crear cadena)")
        print("2. Borrar cadena")
        print("3. Generar texto")
        print("4. Salir")
        choice = int(input("\nIngrese el número: "))

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
                    print("\nNo se pudo guardar la cadena")
                input("\nPresione Enter para continuar...")
                    
            elif choice == 2:
                if not await database.delete_all():
                    print("No se pudo borrar la cadena")
                input("\nPresione Enter para continuar...")
                    
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
                        print_text_result(generated_text)
                    else:
                        print("\nNo se pudo generar el texto")
                        input("\nPresione Enter para continuar...")
                except Exception as e:
                    print(f"\nError al generar texto: {e}")
                    input("\nPresione Enter para continuar...")
                    
            elif choice == 4:
                await database.close()
                break
            else:
                print("\nOpción no válida")
                input("\nPresione Enter para continuar...")
                
        except Exception as e:
            print(f"Error en la operación: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error fatal: {e}")