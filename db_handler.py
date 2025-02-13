import motor.motor_asyncio
import random
from typing import Optional, List, Dict, Any

class DatabaseConnectionError(Exception):
    """Excepción personalizada para errores de conexión"""
    pass

class AsyncDatabaseConnection:
    """Maneja las operaciones asíncronas con la base de datos MongoDB"""
    
    def __init__(self, url: str):
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(url, serverSelectionTimeoutMS=5000)
        except Exception as e:
            raise DatabaseConnectionError(f"Error al inicializar la conexión: {e}")
        self.db = None
        self.collection = None

    async def connect(self, db_name: str, collection_name: str):
        """Establece la conexión con la base de datos y colección especificadas"""
        try:
            # Verifica que la conexión sea válida
            await self.client.server_info()
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            raise DatabaseConnectionError(f"Error al conectar: {e}")

    async def read_all(self) -> List[Dict[str, Any]]:
        """Lee todos los documentos de la colección"""
        try:
            cursor = self.collection.find()
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error al leer documentos: {e}")
            return []

    async def get_next_words(self, chain: list) -> Optional[Dict[str, int]]:
        """Obtiene las posibles siguientes palabras para una cadena dada"""
        try:
            cursor = await self.collection.find_one({"context": chain})
            return cursor["next_words"] if cursor else None
        except Exception as e:
            print(f"Error al obtener siguientes palabras: {e}")
            return None

    async def delete_all(self) -> bool:
        """Elimina todos los documentos de la colección"""
        try:
            result = await self.collection.delete_many({})
            print(f"Se han eliminado {result.deleted_count} documentos.")
            return True
        except Exception as e:
            print(f"Error al eliminar documentos: {e}")
            return False

    async def insert(self, data) -> bool:
        """Inserta uno o varios documentos en la colección"""
        try:
            if isinstance(data, list):
                result = await self.collection.insert_many(data)
            else:
                result = await self.collection.insert_one(data)
            print(f"Se han ingresado {len(result.inserted_ids) if isinstance(data, list) else 1} documentos")
            return True
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            return False

    async def close(self):
        """Cierra la conexión con la base de datos"""
        try:
            self.client.close()
            print("Conexión terminada correctamente.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
