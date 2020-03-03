from questions.views import (
	AdminPanel,
	about,
	contacts,
	main_redirect,
    Game,
    GameMobile,
    get_create_question_form,
	Question,
)
from auth.view import Login


routes = [
    ('GET', '/',                main_redirect,            'main_redirect'),
    ('GET', '/create_question', get_create_question_form, 'create_question_form'),
    ('*',   '/questions',       Question,                 'question'),
    ('*',   '/game',            Game,                     'start_game'),
    ('*',   '/game_mobile',     GameMobile,               'start_game_mobile'),

    ('*', '/admin', AdminPanel, 'admin'),
    ('*', '/login', Login,      'login'),

    ('GET', '/about',    about,    'about'),
    ('GET', '/contacts', contacts, 'contacts')
]
