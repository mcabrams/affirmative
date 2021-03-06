from . import env

ANYMAIL = {
    'MAILGUN_API_KEY': env.MAILGUN_API_KEY,
    'MAILGUN_SENDER_DOMAIN': 'mg.affirmative.site',
}
CELERY_BROKER_URL = 'amqp://broker'
CONFIRMATION_EMAIL = env.CONFIRMATION_EMAIL
DEFAULT_DST_PATH = '/Volumes/dst/'
DOMAIN = env.DOMAIN
PROTOCOL = env.PROTOCOL
REQUEST_CONFIRM_URL = env.REQUEST_CONFIRM_URL
