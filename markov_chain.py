import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import cess_esp
import random
import re

class MarkovChain:
    def __init__(self, n=2):
        self.n = n # Todavia no hace nada.
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

        for i in range(len(tokens_limpios) - 1):
            palabra_actual = tokens_limpios[i]
            palabra_siguiente = tokens_limpios[i + 1]

            if palabra_actual not in self.chain.keys():
                self.chain[palabra_actual] = {palabra_siguiente: 1}
            else:
                if palabra_siguiente not in self.chain[palabra_actual]:
                    self.chain[palabra_actual][palabra_siguiente] = 1
                else:
                    self.chain[palabra_actual][palabra_siguiente] += 1

    def data_to_db(self):
        data = []
        for key, value in self.chain.items():
            data.append({"word": key, "next_words": value})
        return data