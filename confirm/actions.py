import os

from django.conf import settings

from emails.send import send_email

from . import models

EMAIL_ADDRESS = ('notifications@mg.affirmative.site')


def send_confirm_request(confirmation):
    context = {
        'confirmation': confirmation
    }

    send_email('Affirmative?', EMAIL_ADDRESS, [settings.CONFIRMATION_EMAIL],
               'confirm_request', context, html_to_text=True)


def request_confirm(src_path):
    basename = os.path.basename(src_path)
    dst_path = os.path.join(settings.DEFAULT_DST_PATH, basename)
    confirmation = models.Confirmation.objects.create(
        src_path=src_path, dst_path=dst_path)
    send_confirm_request(confirmation)
