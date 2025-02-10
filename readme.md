## Informacion importante antes de utilizar.
- Todavia falta que genere texto, en breve lo termino y pusheo.

- La version de python utilizada es 3.12.8, no puedo confirmar que vaya a funcionar con otras versiones.

- Las librerias necesarias estan en requirements.txt para facilitar la instalacion con pip.

- Se necesita una base de datos mongodb, ademas en el archivo train.py dice

```python 
await database.connect(db_name="totobot", collection_name="transitions")

# Es necesario cambiar totobot y transition por el nombre de la base de datos y de la coleccion en la cual se guardaran las transiciones
```