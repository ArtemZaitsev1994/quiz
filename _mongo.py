import json
from motor import motor_asyncio as ma
from aiohttp.web import Application
from aiofile import AIOFile, Reader

from settings import MONGO_DB_NAME, MONGO_HOST, ADMIN_LOGIN, ADMIN_PASSWORD
from questions.models import Question, NotConfirmedQuestion
from auth.models import Admin


async def _check_admin(app: Application):
    if isinstance(ADMIN_LOGIN, str): 
        if not await app['models']['admin'].get_admin(ADMIN_LOGIN):
            await app['models']['admin'].create_admin(ADMIN_LOGIN, ADMIN_PASSWORD)


def mongo_setup(app: Application):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app['models'] = {
        'questions': Question(app.db),
        'not_conf_q': NotConfirmedQuestion(app.db),
        'admin': Admin(app.db)
    }

    app.on_startup.append(_check_admin)
    app.on_startup.append(fill_db)


async def fill_db(app: Application):
    qs, _ = await app['models']['questions'].get_part(None, 10)
    if len(qs) > 0:
        return

    async with AIOFile('questions.json', 'r') as f:
        questions = json.loads(await f.read())

    await app['models']['questions'].add_questions_many(questions)
