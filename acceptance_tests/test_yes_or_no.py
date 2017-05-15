import requests
from django.core import mail
from base import FunctionalTestCase


class TestYesOrNoTestCase(FunctionalTestCase):
    def test_yes_or_no(self):
        url = self.url('/request-confirm/')
        res = requests.post(url, data={'info': 'Move file x to folder y?'})
        self.assertEqual(res.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Affirmative', mail.outbox[0].subject)
