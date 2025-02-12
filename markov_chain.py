import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import cess_esp
import random
import re

class MarkovChain:
    def __init__(self, n=2):
        self.n = n # Define la longitud de la cadena
        self.chain = {}

    def clear_text(self, texto):
        if isinstance(texto, list):  
            texto = " ".join(texto)

        texto = texto.lower()  # Convertir a minúsculas
        texto = re.sub(r'\d+', '', texto)  # Eliminar números
        texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar puntuación
        texto = re.sub(r'\s+', ' ', texto).strip()  # Eliminar espacios extra
        palabras = word_tokenize(texto, "spanish") 
        return palabras

    def create_transitions(self, texto):
        tokens_limpios = self.clear_text(texto)

        for i in range(len(tokens_limpios) - self.n + 1):
            # Clave: Tupla de (n-1) palabras consecutivas
            clave = tuple(tokens_limpios[i:i+self.n-1])
            """
            Ejemplo con n = 3:
            Si el texto es: ["hola", "como", "estas", "hoy"]
            
            - i = 0 → clave = ("hola", "como")  → siguiente_palabra = "estas"
            - i = 1 → clave = ("como", "estas") → siguiente_palabra = "hoy"
            
            Esto permite construir una cadena de Markov de orden n-1.
            """

            # Palabra que sigue después de la clave
            siguiente_palabra = tokens_limpios[i+self.n-1]

            # Se almacena la relación en el diccionario de transiciones
            if clave not in self.chain:
                self.chain[clave] = {siguiente_palabra: 1}
            else:
                if siguiente_palabra not in self.chain[clave]:
                    self.chain[clave][siguiente_palabra] = 1
                else:
                    self.chain[clave][siguiente_palabra] += 1

    def data_to_db(self):
        data = []
        for key, value in self.chain.items():
            data.append({"context": list(key), "next_words": value})
        return data