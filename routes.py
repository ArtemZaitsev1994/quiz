from questions.views import (
	AdminPanel,
	about,
	contacts,
	main_redirect,
    Game,
    get_create_question_form,
	Question,
)


routes = [
    ('GET', '/',                main_redirect,            'main_redirect'),
    ('*',   '/questions',       Question,                 'question'),
    ('PUT', '/create_question', get_create_question_form, 'create_question_form'),
    ('*',   '/game',            Game,                     'start_game'),

    ('*',   '/admin',    AdminPanel, 'admin'),

    ('GET', '/about',    about,      'about'),
    ('GET', '/contacts', contacts,   'contacts')
]
