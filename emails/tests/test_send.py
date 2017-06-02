import logging
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase

from emails import send


@patch('emails.send.get_email_type')
@patch('emails.send.EmailMultiAlternatives')
class SendEmailTestCase(TestCase):
    subject = sender = tos = filename = 'foo'
    context = {'bar': 'baz'}

    def _expected_context(self):
        return {
            'bar': 'baz',
            'protocol': settings.PROTOCOL,
            'domain': settings.DOMAIN
        }

    def _send_email(self, **kwargs):
        send.send_email(
            self.subject, self.sender, self.tos, self.filename, self.context,
            **kwargs)

    def test_email_recipient_exception_doesnt_raise(self, EMA, _):
        logging.disable(logging.CRITICAL)
        EMA.return_value = instance = Mock()
        instance.send.side_effect = send.EMAIL_RECIPIENT_EXCEPTION()

        self._send_email()
        logging.disable(logging.NOTSET)

    def test_sends_email(self, EMA, _):
        self._send_email()
        EMA().send.assert_called_once_with()

    def test_email_instantiated_properly(self, _, get_email_type):
        Email = get_email_type.return_value
        self._send_email()

        Email.assert_called_once_with(self.filename, self._expected_context())

    def test_email_multi_alt_instantiated_properly(self, EMA, get_email_type):
        Email = get_email_type.return_value
        text = Email.return_value.text = 'lorem'

        self._send_email()

        EMA.assert_called_once_with(
            self.subject, text, self.sender, self.tos)

    def test_html_attached_as_alternative(self, EMA, get_email_type):
        Email = get_email_type.return_value
        html = Email.return_value.html = 'lorem'

        self._send_email()

        EMA().attach_alternative.assert_called_once_with(html, 'text/html')


class GetEmailTypeTestCase(TestCase):
    def test_uses_text_html_email_by_default(self):
        self.assertEqual(send.get_email_type(),
                         send.TextHtmlEmail)

    def test_if_html_to_text_uses_html_to_text_email(self):
        self.assertEqual(send.get_email_type(html_to_text=True),
                         send.HtmlToTextEmail)

    def test_if_not_html_to_text_uses_text_html_email(self):
        self.assertEqual(send.get_email_type(html_to_text=False),
                         send.TextHtmlEmail)


class EmailTestBase:
    filename = 'foo'
    context = {'bar': 'baz'}

    def setUp(self):
        self.email = self.Email(self.filename, self.context)
        patcher = patch('emails.send.render_email')
        self.render_email = patcher.start()
        self.addCleanup(patcher.stop)

    def test_html_renders_email(self, *args):
        self.assertEqual(self.email.html, self.render_email.return_value)

    def test_html_calls_render_properly(self, *args):
        self.email.html
        self.render_email.assert_called_once_with(
            self.filename, self.context, 'html')


class TextHtmlEmailTestCase(EmailTestBase, TestCase):
    Email = send.TextHtmlEmail

    def test_text_renders_email(self):
        self.assertEqual(self.email.text, self.render_email.return_value)

    def test_text_calls_render_properly(self):
        self.email.text
        self.render_email.assert_called_once_with(
            self.filename, self.context, 'txt')


@patch('emails.send.html2text')
class HtmlToTextEmailTestCase(EmailTestBase, TestCase):
    Email = send.HtmlToTextEmail

    def test_text_returns_html_to_text(self, html2text):
        self.assertEqual(self.email.text, html2text.return_value)

    def test_text_calls_html2text_correctly(self, html2text):
        self.email.text
        html2text.assert_called_once_with(self.email.html)


class RenderEmailTestCase(TestCase):
    template, context = 'foo', {'bar': 'baz'}

    @patch('emails.send.render_to_string')
    def test_renders_html_email(self, render):
        actual = send.render_email(self.template, self.context, 'txt')
        self.assertEqual(actual, render())

    @patch('emails.send.render_to_string')
    def test_calls_render_correctly(self, render):
        send.render_email(self.template, self.context, 'mp3')
        args = [send.mail_path(self.template, 'mp3'), self.context]
        render.assert_called_once_with(*args)
