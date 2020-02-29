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

STATIC_PATH = '/static'

if isfile('.env'):
    env.read_envfile('.env')

    DEBUG = env.bool('DEBUG', default=False)

    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_DB_NAME = env.str('MONGO_DB_NAME')

    REDIS_HOST = env.tuple('REDIS_HOST')
else:
    raise SystemExit('Create an env-file please.!')
