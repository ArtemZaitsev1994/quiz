import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp import web

from routes import routes
from middlewares import authorize
from settings import STATIC_PATH, PORT
from _redis import redis_setup, set_redis_session_storage
from _mongo import mongo_setup


## create app
app = web.Application(middlewares=[
    set_redis_session_storage(),
    authorize
])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

## add some urls
for route in routes:
    app.router.add_route(*route[:3], name=route[3])
app.router.add_static(STATIC_PATH, 'static', name='static')
app['static_root_url'] = '/static'

## инициализация redis, также сессии хранятся в редис
redis_setup(app)

## инициализация MongoDB
mongo_setup(app)

## запуск приложения
if __name__ == '__main__':
    web.run_app(app, port=PORT)
