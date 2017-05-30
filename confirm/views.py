from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .actions import send_confirm_request
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
