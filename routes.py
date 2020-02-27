from questions.views import get_rand_question, Question, AdminPanel, admin_redirect, main_redirect, start_game, about


routes = [
    ('GET', '/',                main_redirect,     'main_redirect'),
    ('*',   '/questions',       Question,          'question'),
    ('GET', '/random_question', get_rand_question, 'random_question'),
    ('GET', '/start_game',      start_game,        'start_game'),

    ('*',   '/admin',           AdminPanel,        'admin'),

    ('GET', '/about',           about,             'about')
]
