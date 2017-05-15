from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Confirmation


@csrf_exempt
@require_http_methods(['POST'])
def request_confirm(req):
    if not req.POST or not req.POST.get('info'):
        return HttpResponseBadRequest()

    info = req.POST['info']
    confirmation = Confirmation.objects.create(info=info)
    send_confirm_request(info, confirmation.id)

    return HttpResponse()


def confirm(req, confirmation_id):
    confirmation = Confirmation.objects.get(id=confirmation_id)
    confirmation.confirm()

    return HttpResponse()


def send_confirm_request(confirm_description, confirmation_id):
    text = render_to_string('emails/confirm_request.txt', context={
        'confirm_description': confirm_description,
        'confirmation_id': confirmation_id,
    })

    html = render_to_string('emails/confirm_request.html', context={
        'confirm_description': confirm_description,
        'confirmation_id': confirmation_id,
    })

    send_mail('Affirmative?', text, 'notifications@sandbox8b7c091e63de43b5b29add0f16145485.mailgun.org',
              [settings.CONFIRMATION_EMAIL], html_message=html)
