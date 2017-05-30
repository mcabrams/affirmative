from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch

from confirm import actions
from confirm import models


class RequestConfirm(TestCase):
    @patch('confirm.actions.send_confirm_request')
    def test_creates_confirmation_and_sends(self, send_confirm_request):
        actions.request_confirm('foo')
        confirmation = models.Confirmation.objects.first()
        send_confirm_request.assert_called_once_with('foo', confirmation.id)

    def test_creates_confirmation_with_info(self):
        actions.request_confirm('foo')
        confirmation = models.Confirmation.objects.first()
        self.assertEqual(confirmation.info, 'foo')


class SendConfirmRequestTestCase(TestCase):
    @patch('confirm.actions.send_mail')
    def test_calls_send_mail_properly(self, send_mail_mock):
        actions.send_confirm_request('foobar', 1)

        text = render_to_string('emails/confirm_request.txt', context={
            'confirm_description': 'foobar',
            'confirmation_id': 1,
        })
        html = render_to_string('emails/confirm_request.html', context={
            'confirm_description': 'foobar',
            'confirmation_id': 1,
        })

        send_mail_mock.assert_called_once_with(
            'Affirmative?', text, actions.EMAIL_ADDRESS,
            [settings.CONFIRMATION_EMAIL], html_message=html)

    @override_settings(DOMAIN='foo.com')
    def test_confirmation_links_are_correct_in_email(self):
        confirmation_id = 1
        actions.send_confirm_request('foobar', confirmation_id)
        expected_href = 'foo.com' + reverse('confirm', args=[confirmation_id])
        self.assertIn('<a href="{}">Confirm</a>'.format(expected_href),
                      mail.outbox[0].body)
