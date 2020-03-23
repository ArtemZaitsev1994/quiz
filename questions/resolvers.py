import html
from typing import Any, Dict, List, Optional

import aiohttp_jinja2
from aiohttp import web
from tartiflette import Resolver

from settings import EXCEL_DIR
from questions.utils import set_bold_font


@Resolver("Query.random_question")
async def resolve_query_random_question(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: 'ResolveInfo',
) -> Dict[str, Any]:
    """
    Отдаем рандомный вопрос, приходит список с id уже игравшых вопросов
    """
    # await self.request.app['models']['questions'].clear_db()
    # await self.request.app['models']['not_conf_q'].clear_db()
    print(ctx)
    raise Exception
    q_ids = args['ids']
    q_number = 1
    if q_ids:
        q_ids = q_ids.split('.')
        q_number = len(q_ids) + 1

    qs = await self.request.app['models']['questions'].get_random_question(q_number)

    if len(qs) <= len(q_ids):
        return web.json_response({'warning': 'no more questions'})

    q = next((x for x in qs if str(x['_id']) not in q_ids))
    for key in ['text', 'answer']:
        q[key] = html.unescape(set_bold_font(q[key]))
    return web.json_response(q)


class Question(web.View):

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

        if data.get('questions'):
            result = web.json_response(await self.request.app['models'][q_type].update_question(data))
        else:
            result = web.json_response(await self.request.app['models'][q_type].add_question(data))
            if data.get('not_conf_q'):
                await self.request.app['models']['not_conf_q'].delete_q(data['not_conf_q'])

        return web.json_response(bool(result))


class AdminPanel(web.View):

    @aiohttp_jinja2.template('admin/questions.html')
    async def get(self):
        """Получаем по 10 предложенных вопросов"""
        PER_PAGE = 10
        page = self.request.rel_url.query.get('page', 1)
        model = self.request.rel_url.query.get('model', 'not_conf_q')
        all_models = [(x.NAME, x.INTERNAL_NAME) for x in self.request.app['models'].values()]

        try:
            page = int(page)
        except ValueError:
            return web.HTTPBadRequest()
        if page < 0:
            page *= -1
        qs, pagination = await self.request.app['models'][model].get_part(page, PER_PAGE)
        for i in ('prev', 'next'):
            if pagination[i] is not None:
                pagination[i] = self.request.app.router['admin'].url_for().with_query({'model': model, 'page': pagination[i]})

        return {'questions': qs, 'pagination': pagination, 'model': model, 'all_models': all_models}

    async def delete(self):
        """Удаление вопроса из предложенных"""
        json_data = await self.request.json()
        return web.json_response(await self.request.app['models'][json_data['model']].delete_q(json_data['id']))


class Game(web.View):

    @aiohttp_jinja2.template('question.html')
    async def get(self):
        """Стартует игру, отдает 6 вопросов"""
        qs = await self.request.app['models']['questions'].get_random_question(4)
        for q in qs:
            for key in ['text', 'answer']:
                q[key] = set_bold_font(html.unescape(q[key]))
        return {'questions': qs, 'q_ids': '.'.join([q['_id'] for q in qs])}


class GameMobile(web.View):

    async def get(self):
        """Стартует игру, отдает 6 вопросов"""
        qs = await self.request.app['models']['questions'].get_random_question(4)
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
