import html

import aiohttp_jinja2
from aiohttp import web


class Question(web.View):

    @aiohttp_jinja2.template('add_question.html')
    async def get(self):
        qs = await app['models']['questions'].get_rand_question(6)
        return web.json_response(qs)

    async def post(self):
        data = self.request.json()
        for key in ['text', 'answer']:
            data[key] = html.escape(data[key], quote=True)
        data['complexity'] = int(data['complexity'])

        return web.json_response(await app['models']['questions'].add_question(data))


class NotConfirmedQuestion(web.View):

    @aiohttp_jinja2.template('admin/questions.html')
    async def get(self):
        PER_PAGE = 10
        page = self.request.json().page or None
        qs = await app['models']['not_conf_q'].get_part(page, PER_PAGE)

        return web.json_response(qs)

    async def post(self):
        data = self.request.json()
        for key in ['text', 'answer']:
            data[key] = html.escape(data[key], quote=True)
        data['complexity'] = int(data['complexity'])

        return web.json_response(await app['models']['questions'].add_question(data))


async def get_rand_question(request):
    qs = await app['models']['questions'].get_rand_question(1)
    return web.json_response(qs)


async def main_redirect(request):
    location = request.app.router['question'].url_for()
    raise web.HTTPFound(location=location)


async def admin_redirect(request):
    location = request.app.router['not_conf_q'].url_for()
    raise web.HTTPFound(location=location)
