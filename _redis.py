from typing import Callable

import aioredis
import asyncio
from aiohttp.web import Application
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage

from settings import REDIS_HOST, SESSION_TTL


async def make_redis_pool():
    redis_address = REDIS_HOST
    return await aioredis.create_pool(
        redis_address,
        create_connection_timeout=1,
    )


def set_redis_session_storage() -> Callable:
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(redis_pool, max_age=SESSION_TTL)
    return session_middleware(storage)


async def create_redis(app: Application):
    app['redis'] = await aioredis.create_redis(REDIS_HOST)
    app['redis'].decode_response = True


async def close_redis(app: Application):
    app['redis'].close()
    await app['redis'].wait_closed()


def redis_setup(app: Application):
    app.on_startup.append(create_redis)
    app.on_cleanup.append(close_redis)
