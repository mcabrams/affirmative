from .utility import env_get_or_warn

CONFIRMATION_EMAIL = env_get_or_warn('CONFIRMATION_EMAIL')
MAILGUN_API_KEY = env_get_or_warn('MAILGUN_API_KEY'),
SECRET_KEY = env_get_or_warn('SECRET_KEY')
DOMAIN = env_get_or_warn('DOMAIN')
