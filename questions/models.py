from typing import Dict, List, Any

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import QUESTION_COLLECTION, NOT_CONFIRMED_QUESTION_COLLECTION


class BaseQuestion:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = NotImplementedError

    async def add_question(self, data) -> bool:
        keys = {'category', 'text', 'complexity', 'answer'}
        if len(keys - set(data.keys())) != 0:
            return False
        return bool(await self.collection.insert_one(data))

    async def add_questions_many(self, questions) -> bool:
        keys = {'category', 'text', 'complexity', 'answer'}
        valid_q = [x for x in questions if len(keys - set(x.keys())) == 0]
        print(valid_q)
        return bool(await self.collection.insert_many(valid_q))


    async def update_question(self, data) -> bool:
        return bool(await self.collection.update_one(
            {'_id': ObjectId(data.pop('questions'))},
            {'$set': data}
        ))

    async def get_part(self, page, per_page) -> List[Dict[str, Any]]:
        page = page or 1
        all_qs = self.collection.find()
        count_qs = await self.collection.count_documents({})
        has_next = count_qs > 10
        qs = await all_qs.skip((page - 1) * per_page).limit(per_page).to_list(length=None)
        
        pagination = {
            'has_next': has_next,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if has_next else None,
            'page': page,
            'per_page': per_page,
            'max': count_qs // per_page if count_qs % per_page == 0 else count_qs // per_page + 1
        }

        return qs, pagination

    async def get_random_question(self, count) -> Dict[str, Any]:
        qs = await self.collection.aggregate([{ '$sample': { 'size': count} }]).to_list(length=None)
        for q in qs:
            q['_id'] = str(q['_id'])
        return qs

    async def delete_q(self, _id) -> bool:
        result = await self.collection.delete_many({'_id': ObjectId(_id)})
        return bool(result)

    async def clear_db(self):
        await self.collection.drop()


class Question(BaseQuestion):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[QUESTION_COLLECTION]


class NotConfirmedQuestion(BaseQuestion):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[NOT_CONFIRMED_QUESTION_COLLECTION]