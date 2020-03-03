import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp import web
from motor import motor_asyncio as ma
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_session import session_middleware

from routes import routes
from middlewares import authorize
from settings import MONGO_DB_NAME, MONGO_HOST, STATIC_PATH
from questions.models import Question, NotConfirmedQuestion
from auth.models import Admin
from utils import make_redis_pool, create_redis, close_redis, _check_admin


loop = asyncio.get_event_loop()
redis_pool = loop.run_until_complete(make_redis_pool())
storage = RedisStorage(redis_pool)
session_redis_middleware = session_middleware(storage)

app = web.Application(middlewares=[session_redis_middleware, authorize])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# add some urls
for route in routes:
    app.router.add_route(*route[:3], name=route[3])
app.router.add_static(STATIC_PATH, 'static', name='static')
app['static_root_url'] = '/static'

app.client = ma.AsyncIOMotorClient(MONGO_HOST)
app.db = app.client[MONGO_DB_NAME]

app['models'] = {
	'questions': Question(app.db),
	'not_conf_q': NotConfirmedQuestion(app.db),
	'admin': Admin(app.db)
}

app.on_startup.append(create_redis)
app.on_startup.append(_check_admin)
app.on_cleanup.append(close_redis)

web.run_app(app)
