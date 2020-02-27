import asyncio
import aiohttp_jinja2
import jinja2
from motor import motor_asyncio as ma

from aiohttp import web
from routes import routes
from settings import MONGO_DB_NAME, MONGO_HOST, STATIC_PATH
from questions.models import Question, NotConfirmedQuestion

loop = asyncio.get_event_loop()

app = web.Application()
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
	'not_conf_q': NotConfirmedQuestion(app.db)
}

web.run_app(app)
