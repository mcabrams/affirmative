from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from . import models


EMAIL_ADDRESS = ('notifications@mg.affirmative.site')


def send_confirm_request(confirm_description, confirmation_id):
    text = render_to_string('emails/confirm_request.txt', context={
        'confirm_description': confirm_description,
        'confirmation_id': confirmation_id,
    })

    html = render_to_string('emails/confirm_request.html', context={
        'confirm_description': confirm_description,
        'confirmation_id': confirmation_id,
    })

    send_mail('Affirmative?', text, EMAIL_ADDRESS,
              [settings.CONFIRMATION_EMAIL], html_message=html)


def request_confirm(info):
    confirmation = models.Confirmation.objects.create(info=info)
    send_confirm_request(info, confirmation.id)
