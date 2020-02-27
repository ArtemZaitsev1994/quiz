from questions.views import (
	AdminPanel,
	about,
	contacts,
	main_redirect,
	get_rand_question,
	start_game,
	Question,
)


routes = [
    ('GET', '/',                main_redirect,     'main_redirect'),
    ('*',   '/questions',       Question,          'question'),
    ('PUT', '/random_question', get_rand_question, 'random_question'),
    ('GET', '/start_game',      start_game,        'start_game'),

    ('*',   '/admin',           AdminPanel,        'admin'),

    ('GET', '/about',           about,             'about'),
    ('GET', '/contacts',        contacts,          'contacts')
]
