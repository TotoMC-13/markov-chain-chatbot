import motor.motor_asyncio
import random

class AsyncDatabaseConnection:
    def __init__(self, url: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = None
        self.collection = None

    async def connect(self, db_name: str, collection_name: str):
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def read_all(self):
        cursor = self.collection.find()
        return await cursor.to_list(length=None)
    
    async def get_next_words(self, chain: list):
        cursor = await self.collection.find_one({"context": chain})
        return cursor["next_words"] if cursor else None

    async def delete_all(self):
        result = await self.collection.delete_many({})
        print(f"Se han eliminado {result.deleted_count} documentos.")

    async def insert(self, data):
        if isinstance(data, list):
            result = await self.collection.insert_many(data)
        else:
            result = await self.collection.insert_one(data)
        print(f"Se han ingresado {len(result.inserted_ids)}")

    async def close(self):
        self.client.close()
        print("Conexión terminada.")
