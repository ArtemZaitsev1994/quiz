import aioredis

from settings import REDIS_HOST


async def make_redis_pool():
    redis_address = REDIS_HOST
    return await aioredis.create_pool(
        redis_address,
        create_connection_timeout=1,
    )
