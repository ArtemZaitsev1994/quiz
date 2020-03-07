import aiohttp_jinja2
from aiohttp_session import get_session, new_session
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
                session = await new_session(self.request)
                await set_session(session, self.request.app['redis'], admin['login'])
                return web.json_response({'location': str(self.request.app.router['admin'].url_for())})
        return web.json_response({'error': 'wrong pass or name'})

    async def delete(self):
        session = await get_session(self.request)
        if session.get('admin_token'):
            await self.request.app['redis'].delete(session.get('admin_token'))
            session.invalidate()

        return web.json_response({'location': str(self.request.app.router['about'].url_for())})
