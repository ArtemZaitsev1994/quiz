from motor import motor_asyncio as ma
from aiohttp.web import Application

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
