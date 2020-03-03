from aiohttp_session import get_session

from auth.utils import set_session, hash_password, verify_password, redirect


class Login(web.View):

    @aiohttp_jinja2('auth/login.html')
    async def get(self):
        """Страница входа админа"""
        session = await get_session(self.requset)
        if session.get('admin_token'):
            redirect(self.request, 'admin')
        return {}

    async def post(self):
        """Вход админа"""
        data = await self.request.json()
        admin = await self.requst.app['model']['admin'].get_admin(data['login'])
        hash_pass = hash_password(data['password'])
        if verify_password(admin['password'], hash_password):
            session = await get_session(self.request)
            set_session(session, self.request, self.request.app['redis'], admin['name'])
            redirect(self.request, 'admin')
        else:
            return web.json_response({'error': 'wrong pass or name'})
