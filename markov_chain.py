import nltk
from db_handler import AsyncDatabaseConnection
from nltk.tokenize import word_tokenize
from nltk.corpus import cess_esp
import random
import re

class MarkovChain:
    def __init__(self, n=2):
        self.n = n  # Define la longitud de la cadena
        self.chain = {}
        self.STOP_WORDS = {"y", "de", "el", "la", "los", "las", "en", "con", 
                          "para", "por", "que", "a", "o", "e", "un", "una", "del"}

    def clear_text(self, text):
        if isinstance(text, list):  
            text = " ".join(text)

        text = text.lower()  # Convertir a minúsculas
        text = re.sub(r'\d+', '', text)  # Eliminar números
        text = re.sub(r'[^\w\s]', '', text)  # Eliminar puntuación
        text = re.sub(r'\s+', ' ', text).strip()  # Eliminar espacios extra
        words = word_tokenize(text, "spanish") 
        return words

    def create_transitions(self, text):
        clean_tokens = self.clear_text(text)

        for i in range(len(clean_tokens) - self.n + 1):
            # Clave: Tupla de (n-1) palabras consecutivas
            key = tuple(clean_tokens[i:i+self.n-1])
            """
            Ejemplo con n = 3:
            Si el texto es: ["hola", "como", "estas", "hoy"]
            
            - i = 0 → key = ("hola", "como") → next_word = "estas"
            - i = 1 → key = ("como", "estas") → next_word = "hoy"
            
            Esto construye una cadena de Markov de orden n-1.
            """

            # Palabra que sigue después de la clave
            next_word = clean_tokens[i+self.n-1]

            # Almacena la relación en el diccionario de transiciones
            if key not in self.chain:
                self.chain[key] = {next_word: 1}
            else:
                if next_word not in self.chain[key]:
                    self.chain[key][next_word] = 1
                else:
                    self.chain[key][next_word] += 1

    async def generate_text(self, database, initial_chain, max_length=50):
        text = []
        chain = initial_chain

        while len(text) < max_length or text[-1] in self.STOP_WORDS:
            next_words = await database.get_next_words(chain=chain)
            next_word = self.get_next_word(chain, next_words)
            
            if not next_word:
                break
                
            text.append(next_word)
            
            if self.n > 2:
                chain = chain[-(self.n - 2):] + [next_word]
            else:
                chain = [next_word]

        return text

    def get_next_word(self, chain: list, all_words: dict):
        """Usa las probabilidades de la cadena de Markov para elegir la siguiente palabra"""
        if not all_words:  
            return None  # Si no hay coincidencia

        words, weights = zip(*all_words.items())  # Extrae palabras y probabilidades
        return random.choices(words, weights=weights)[0]  # Devuelve una palabra aleatoria

    def data_to_db(self):
        data = []
        for key, value in self.chain.items():
            data.append({"context": list(key), "next_words": value})
        return data