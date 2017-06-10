import os

from django.conf import settings

from . import models


def request_confirm(src_path):
    basename = os.path.basename(src_path)
    dst_path = os.path.join(settings.DEFAULT_DST_PATH, basename)
    models.Confirmation.objects.create(src_path=src_path, dst_path=dst_path)
