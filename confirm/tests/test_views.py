from unittest.mock import patch


from django.conf import settings
from django.core import mail
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from django.urls import reverse

from confirm.models import Confirmation
from confirm.views import send_confirm_request


class RequestConfirmTestCase(TestCase):
    url = reverse('request_confirm')

    def test_does_not_accept_requests_that_are_not_POST(self):
        request_types = ('delete', 'get', 'head', 'patch', 'put',)

        for request_type in request_types:
            with self.subTest(request_type=request_type):
                request_method = getattr(self.client, request_type)
                res = request_method(self.url, {'info': 'foobar'})
                self.assertIsInstance(res, HttpResponseNotAllowed)

    def test_not_passing_POST_data_returns_bad_response(self):
        res = self.client.post(self.url)
        self.assertIsInstance(res, HttpResponseBadRequest)

    def test_not_passing_info_returns_bad_response(self):
        res = self.client.post(self.url, {'notright': 'foobar'})
        self.assertIsInstance(res, HttpResponseBadRequest)

    def test_responds_to_POST_request_with_info_OK(self):
        res = self.client.post(self.url, {'info': 'foobar'})
        self.assertEqual(res.status_code, 200)

    def test_creates_confirmation_with_info(self):
        self.client.post(self.url, {'info': 'foobar'})
        count = Confirmation.objects.filter(info='foobar').count()
        self.assertEqual(count, 1)

    @patch('confirm.views.send_confirm_request')
    def test_queues_email_with_info(self, send_mock):
        self.client.post(self.url, {'info': 'foobar'})
        confirmation = Confirmation.objects.filter(info='foobar').first()
        send_mock.assert_called_once_with('foobar', confirmation.id)


class ConfirmTestCase(TestCase):
    def test_can_confirm_request(self):
        confirmation = Confirmation.objects.create()
        url = reverse('confirm', args=[confirmation.id])
        self.client.get(url)
        confirmation.refresh_from_db()
        self.assertTrue(confirmation.confirmed)


class SendConfirmRequestTestCase(TestCase):
    @patch('confirm.views.send_mail')
    def test_calls_send_mail_properly(self, send_mail_mock):
        send_confirm_request('foobar', 1)

        text = render_to_string('emails/confirm_request.txt', context={
            'confirm_description': 'foobar',
            'confirmation_id': 1,
        })
        html = render_to_string('emails/confirm_request.html', context={
            'confirm_description': 'foobar',
            'confirmation_id': 1,
        })

        send_mail_mock.assert_called_once_with(
            'Affirmative?',
            text,
            'notifications@sandbox8b7c091e63de43b5b29add0f16145485.mailgun.org',
            [settings.CONFIRMATION_EMAIL],
            html_message=html)

    @override_settings(DOMAIN='foo.com')
    def test_confirmation_links_are_correct_in_email(self):
        confirmation_id = 1
        send_confirm_request('foobar', confirmation_id)
        expected_href = 'foo.com' + reverse('confirm', args=[confirmation_id])
        self.assertIn('<a href="{}">Confirm</a>'.format(expected_href),
                      mail.outbox[0].body)
