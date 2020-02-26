from question.views import get_rand_question, Question, NotConfirmedQuestion, admin_redirect, main_redirect


routes = [
    ('GET', '/',                main_redirect,        'main_redirect'),
    ('*',   '/questions',       Question,             'question'),
    ('GET', '/random_question', get_rand_question,    'random_question'),

    ('GET', '/admin',           admin_redirect,       'admin'),
    ('*',   '/admin/questions', NotConfirmedQuestion, 'not_conf_q')
]
