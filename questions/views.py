import html

import aiohttp_jinja2
from aiohttp import web


class Question(web.View):

    @aiohttp_jinja2.template('add_question.html')
    async def get(self):
        return {}

    async def post(self):
        data = await self.request.json()

        q_type = data.pop('type')
        # проверка на админа
        if q_type == 'questions' and False:
            return web.json_response({'error': 'Access denied'})

        for key in ['text', 'answer']:
            data[key] = html.escape(data[key], quote=True)
        data['complexity'] = int(data['complexity'])

        result = web.json_response(await self.request.app['models'][q_type].add_question(data))
        if data.get('not_conf_id'):
            await self.request.app['models']['not_conf_q'].delete_q(data['not_conf_id'])

        return web.json_response(bool(result))


class AdminPanel(web.View):

    @aiohttp_jinja2.template('admin/questions.html')
    async def get(self):
        PER_PAGE = 10
        page = self.request.rel_url.query.get('page', 1)
        try:
            page = int(page)
        except ValueError:
            return web.HTTPBadRequest()
        if page < 0:
            page *= -1
        qs, pagination = await self.request.app['models']['not_conf_q'].get_part(page, PER_PAGE)

        return {'questions': qs, 'pagination': pagination}

    async def delete(self):
        json_data = await self.request.json()
        return await self.request.app['models']['not_conf_q'].delete_q(json_data['id'])


@aiohttp_jinja2.template('question.html')
async def start_game(request):
    qs = await request.app['models']['questions'].get_random_question(3)
    return {'questions': qs, 'q_ids': '.'.join([q['_id'] for q in qs])}

async def get_rand_question(request):
    q_number = 1
    q_ids = (await request.json()).get('ids')
    if q_ids:
        q_number = len(q_ids) + 1
    qs = await request.app['models']['questions'].get_random_question(q_number)
    if len(qs) <= len(q_ids):
        return web.json_response({'warning': 'no more questions'})
    q = next((x for x in qs if str(x['_id']) not in q_ids))
    return web.json_response(q)


async def main_redirect(request):
    location = request.app.router['question'].url_for()
    raise web.HTTPFound(location=location)


@aiohttp_jinja2.template('about.html')
async def about(request):
    return {}


@aiohttp_jinja2.template('contacts.html')
async def contacts(request):
    return {}