import logging
import os
from os.path import isfile
from envparse import env

log = logging.getLogger('quiz')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

QUESTION_COLLECTION = 'quiz_questions'
NOT_CONFIRMED_QUESTION_COLLECTION = 'not_confirmed_quiz_questions'
ADMIN_COLLECTION = 'admin'

STATIC_PATH = '/static'

if isfile('.env'):
    env.read_envfile('.env')

    DEBUG = env.bool('DEBUG', default=False)

    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_DB_NAME = env.str('MONGO_DB_NAME')

    REDIS_HOST = env.tuple('REDIS_HOST')
    SESSION_TTL = env.int('SESSION_TTL')

    EXCEL_DIR = env.str('EXCEL_DIR')

    PORT = env.int('PORT')

    try:
        ADMIN_LOGIN = env.str('ADMIN_LOGIN')
        ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
    except envparse.ConfigurationError:
        ADMIN_PASSWORD, ADMIN_LOGIN = None, None
else:
    raise SystemExit('Create an env-file please.!')
