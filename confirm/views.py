from django.http import HttpResponse
from django.shortcuts import render

from .actions import copy_to_destination
from .forms import ConfirmFormset
from .models import Confirmation


def confirm(request, confirmation_id):
    confirmation = Confirmation.objects.get(id=confirmation_id)
    copy_to_destination(confirmation.src_path, confirmation.dst_path)
    confirmation.confirm()

    return HttpResponse()


def confirms(request):
    return render(request, 'confirms.html', {
        'formset': ConfirmFormset()
    })
