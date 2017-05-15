from django import template
from django.conf import settings
from django.urls import reverse

register = template.Library()


@register.simple_tag
def url_with_domain(url, *args, **kwargs):
    return settings.DOMAIN + reverse(url, args=args, kwargs=kwargs)
