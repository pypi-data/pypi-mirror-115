from fastapi.exceptions import HTTPException
import motor.motor_asyncio

class Database():

    def __init__(self, db_url, db_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]


    async def db_check_connection(self) -> int:

        try:
            await self.client.admin.command("serverStatus")
            await self.db.command('ping')
            return 200
            
        except Exception:
            return 503

    async def insert_one(self, pydantic_object):

        content_dict = dict(pydantic_object)
        collection = pydantic_object.__class__.__name__

        await self.db[collection].insert_one(content_dict)

    async def find_one(self, pydantic_object):

        content_dict = dict(pydantic_object)
        collection = pydantic_object.__class__.__name__
        # find_one({"_id": new_student.inserted_id})
        
        if (query_result := await self.db[collection].find_one(content_dict, )) is not None:
            return query_result
        else:
            raise HTTPException(404)
    

    def shutdown_database(self):
        self.client.close()


    def __del__(self):
        self.shutdown_database()