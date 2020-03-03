import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web

from auth.utils import set_session, hash_password, verify_password, redirect


class Login(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        """Страница входа админа"""
        session = await get_session(self.request)
        if session.get('admin_token'):
            redirect(self.request, 'admin')
        return {}

    async def post(self):
        """Вход админа"""
        data = await self.request.json()
        admin = await self.request.app['models']['admin'].get_admin(data['login'])
        if admin is not None:
            if verify_password(admin['password'], data['password']):
                session = await get_session(self.request)
                await set_session(session, self.request.app['redis'], admin['login'])
                redirect(self.request, 'admin')
        return web.json_response({'error': 'wrong pass or name'})
