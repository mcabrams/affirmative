import logging

from anymail import exceptions
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from html2text import html2text

logger = logging.getLogger(__name__)

EMAIL_RECIPIENT_EXCEPTION = exceptions.AnymailRecipientsRefused


def send_email(subject, sender, tos, filename, context, html_to_text=False):
    context = _add_domain_info_to_context(context)

    Email = get_email_type(html_to_text)
    email = Email(filename, context)
    message = EmailMultiAlternatives(subject, email.text, sender, tos)
    message.attach_alternative(email.html, 'text/html')

    try:
        message.send()
    except EMAIL_RECIPIENT_EXCEPTION as exc:
        """ If an email bounced, we aren't going to be able to deliver that
        message at later date, so we log warning and continue. """

        logger.warning('{exc}: Exception sending email with subject'
                       ' "{subject}" to {tos}'.format(exc=str(exc),
                                                      subject=subject,
                                                      tos=tos))
        pass


def _add_domain_info_to_context(context):
    context = context.copy()
    context.update({
        'protocol': settings.PROTOCOL,
        'domain': settings.DOMAIN,
    })
    return context


def get_email_type(html_to_text=False):
    return HtmlToTextEmail if html_to_text else TextHtmlEmail


class Email:
    def __init__(self, filename, context):
        self.filename = filename
        self.context = context

    @property
    def html(self):
        return render_email(self.filename, self.context, 'html')


class TextHtmlEmail(Email):
    """ Class for emails that have a txt and html template """
    @property
    def text(self):
        return render_email(self.filename, self.context, 'txt')


class HtmlToTextEmail(Email):
    """ Class for emails that have an html template, and use html2string
    to generate text representation from html template """
    @property
    def text(self):
        return html2text(self.html)


def render_email(filename, context, filetype):
    path = mail_path(filename, filetype)
    return render_to_string(path, context)


def mail_path(filename, filetype):
    return 'emails/{}.{}'.format(filename, filetype)
