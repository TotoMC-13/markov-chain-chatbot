# Generador de Texto con Cadenas de Markov

Este proyecto implementa un generador de texto basado en Cadenas de Markov utilizando el corpus CESS-ESP y CoNLL-2002 de NLTK.

## Requisitos Previos

- Python 3.12.8, no se si funciona con otras versiones
- MongoDB
- Las librerías especificadas en requirements.txt

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos:
   - Crear una variable de entorno en .env `DB_URL` con la URL de conexión a MongoDB
   - O modificar directamente en `train.py`:
```python
url = "mongodb://localhost:27017"  # Reemplazar con tu URL
```

4. Descargar recursos NLTK:
   - Descomentar las siguientes líneas en `train.py` en la primera ejecución:
```python
nltk.download('cess_esp')    # Corpus en español general
nltk.download('conll2002')   # Corpus de noticias en español
nltk.download('punkt')       # Tokenizador de oraciones
```

## Uso

1. **Entrenar el modelo**:
   - Seleccionar opción 1
   - Ingresar longitud de cadena (mínimo 2)
   - El sistema entrenará usando el/los corpus seleccionado/s

2. **Generar texto**:
   - Seleccionar opción 3
   - Ingresar longitud de cadena (tiene que ser la misma longitud con la que se entreno, para cambiarla es necesario borrar las transiciones y crear nuevas)
   - El sistema generará texto basado en el entrenamiento

3. **Borrar datos**:
   - Seleccionar opción 2 para eliminar el entrenamiento

## Estructura del Proyecto

- `train.py`: Programa principal
- `markov_chain.py`: Implementación de la cadena de Markov
- `db_handler.py`: Manejo de la base de datos
- `requirements.txt`: Dependencias del proyecto

## Configuración de la Base de Datos

En el archivo `train.py`, busca la siguiente línea:

```python
await database.connect(db_name="totobot", collection_name="transitions")
```

Y reemplaza:
- `"totobot"` por el nombre de tu base de datos
- `"transitions"` por el nombre de la colección donde se guardarán los datos

Por ejemplo, si tu base de datos se llama "miproyecto" y quieres usar una colección llamada "markov_data":

```python
await database.connect(db_name="miproyecto", collection_name="markov_data")
```

> **Importante**: Este cambio debe hacerse antes de ejecutar el programa por primera vez, ya que determina dónde se guardarán los datos de entrenamiento.

## Detalles Técnicos

### Funcionamiento
- Utiliza Cadenas de Markov para generar texto basado en probabilidades
- La longitud de la cadena (n) determina cuántas palabras previas se consideran para predecir la siguiente
- El texto generado tiene una longitud mínima de 50 palabras y evita terminar en palabras conectoras

### Almacenamiento
- MongoDB guarda las transiciones en formato:
```json
{
    "context": ["palabra1", "palabra2"],
    "next_words": {
        "palabra3": 1,
        "palabra4": 2
    }
}
```

### Consideraciones
- A mayor longitud de cadena, más coherente pero menos creativo será el texto
- Es necesario mantener la misma longitud de cadena al entrenar y generar
- El corpus CESS-ESP proporciona un conjunto limitado de textos en español

## Corpus Disponibles

El sistema soporta los siguientes corpus en español de NLTK:

1. **CESS-ESP**: Corpus general del español
   - Incluye textos variados y anotados
   - Mejor para generación de texto general

2. **CoNLL-2002**: Corpus de noticias en español
   - Contiene textos periodísticos
   - Mejor para generar texto formal o de noticias

3. **Combinado**: Todos los corpus anteriores juntos
   - Mayor variedad de vocabulario
   - Puede generar textos más diversos

## Limitaciones Conocidas

- Solo funciona con texto en español
- Requiere memoria suficiente para el corpus
- La calidad del texto depende del entrenamiento

## Contribuciones

Siéntete libre de contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para features
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
