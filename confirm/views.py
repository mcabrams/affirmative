from django.http import HttpResponse

from .actions import copy_to_destination
from .models import Confirmation


def confirm(req, confirmation_id):
    confirmation = Confirmation.objects.get(id=confirmation_id)
    copy_to_destination(confirmation.src_path, confirmation.dst_path)
    confirmation.confirm()

    return HttpResponse()
