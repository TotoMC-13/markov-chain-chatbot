import motor.motor_asyncio

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
        documents = await cursor.to_list(length=None)
        for doc in documents:
            print(doc)

    async def insert(self, data):
        if isinstance(data, list):
            await self.collection.insert_many(data)
        else:
            await self.collection.insert_one(data)

    async def close(self):
        self.client.close()
        print("Conexión terminada.")
