import hashlib
import binascii
import os
import uuid

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_session import Session
from aioredis import Redis
from settings import SESSION_TTL


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        100000
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def redirect(request: Request, router_name: str):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


async def set_session(session: Session, redis: Redis, name: str):
    session_uuid = uuid.uuid4().hex
    session['admin_token'] = session_uuid
    await redis.set(session_uuid, name)
    await redis.expire(session_uuid, SESSION_TTL)
