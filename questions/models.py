from typing import Dict, List, Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import QUESTION_COLLECTION, NOT_CONFIRMED_QUESTION_COLLECTION


class Question:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = self.db[QUESTION_COLLECTION]

    async def get_random_question(self, count) -> Dict[str, Any]:
        q = self.collection.aggregate([{ '$sample': { 'size': count} }])
        q['_id'] = str(q['_id'])
        return q

    async def add_question(self, data) -> bool:
        keys = {'category', 'text', 'complexity'}
        if len(keys - set(data.keys())) != 0:
            return False
        return bool(await self.collection.insert(data))


class NotConfirmedQuestion:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = self.db[NOT_CONFIRMED_QUESTION_COLLECTION]

    async def get_part(self, page, per_page) -> List[Dict[str, Any]]:
        page = page or 1
        return await self.collection.find().skip(page * per_page).limit(per_page).to_list(length=None)

    async def add_question(self, data) -> bool:
        keys = {'category', 'text', 'complexity', 'answer'}
        if len(keys - set(data.keys())) != 0:
            return False
        return bool(await self.collection.insert(data))
