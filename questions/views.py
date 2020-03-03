import html

import aiohttp_jinja2
from aiohttp import web

from settings import EXCEL_DIR


class Question(web.View):

    async def get(self):
        """Отдаем рандомный вопрос, приходит список с id уже игравшых вопросов"""
        # await self.request.app['models']['questions'].clear_db()
        q_ids = self.request.rel_url.query.get('ids', [])
        q_number = 1
        if q_ids:
            q_ids = q_ids.split('.')
            q_number = len(q_ids) + 1

        qs = await self.request.app['models']['questions'].get_random_question(q_number)

        if len(qs) <= len(q_ids):
            return web.json_response({'warning': 'no more questions'})

        q = next((x for x in qs if str(x['_id']) not in q_ids))
        return web.json_response(q)

    async def post(self):
        """Создание вопроса"""
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
        """Получаем по 10 предложенных вопросов"""
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
        """Удаление вопроса из предложенных"""
        json_data = await self.request.json()
        return await self.request.app['models']['not_conf_q'].delete_q(json_data['id'])


class Game(web.View):

    @aiohttp_jinja2.template('question.html')
    async def get(self):
        """Стартует игру, отдает 6 вопросов"""
        qs = await self.request.app['models']['questions'].get_random_question(3)
        return {'questions': qs, 'q_ids': '.'.join([q['_id'] for q in qs])}


class GameMobile(web.View):

    async def get(self):
        """Стартует игру, отдает 6 вопросов"""
        qs = await self.request.app['models']['questions'].get_random_question(3)
        return web.json_response(qs)


class ExcelView(web.View):

    async def post(self):
        data = await self.request.post()

        if not os.path.exists(EXCEL_DIR):
            os.makedir(EXCEL_DIR)

        filename = len(next(os.walk(EXCEL_DIR))[2]) + 1
        input_file = data['file'].file

        with open(os.path.join(EXCEL_DIR, f'{filename}.xlsx'), 'wb') as f:
            f.write(input_file.read())

        link = self.request.app.router['upload'].url_for().with_query({'file': filename})
        return web.json_response({'link': link})



@aiohttp_jinja2.template('create_question_form.html')
async def get_create_question_form(request):
    return {}


@aiohttp_jinja2.template('about.html')
async def about(request):
    return {}


@aiohttp_jinja2.template('contacts.html')
async def contacts(request):
    return {}


async def main_redirect(request):
    location = request.app.router['start_game'].url_for()
    raise web.HTTPFound(location=location)
