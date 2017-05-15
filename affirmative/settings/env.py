from .utility import env_get_or_warn

CONFIRMATION_EMAIL = env_get_or_warn('CONFIRMATION_EMAIL')

ANYMAIL = {
    'MAILGUN_API_KEY': env_get_or_warn('MAILGUN_API_KEY'),
}
