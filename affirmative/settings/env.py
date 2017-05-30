from .utility import env_get_or_warn

CONFIRMATION_EMAIL = env_get_or_warn('CONFIRMATION_EMAIL')
DOMAIN = env_get_or_warn('DOMAIN')
MAILGUN_API_KEY = env_get_or_warn('MAILGUN_API_KEY')
REQUEST_CONFIRM_URL = env_get_or_warn('REQUEST_CONFIRM_URL')
SECRET_KEY = env_get_or_warn('SECRET_KEY')
