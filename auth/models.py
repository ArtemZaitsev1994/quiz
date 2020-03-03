from typing import Dict

from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import ADMIN_COLLECTION


class Admin:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db[ADMIN_COLLECTION]

    async def create_admin(self):
        pass

    async def check_admin(self):
        pass

    async def del_admin(self):
        pass

    async def get_admin(self, login):
        return self.collection.find_one({'login': login})