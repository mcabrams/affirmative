from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from confirm.models import Confirmation


@patch('confirm.views.copy_to_destination')
class ConfirmTestCase(TestCase):
    def test_can_confirm_request(self, _):
        confirmation = Confirmation.objects.create()
        url = reverse('confirm', args=[confirmation.id])
        self.client.get(url)
        confirmation.refresh_from_db()
        self.assertTrue(confirmation.confirmed)

    def test_copies_path(self, copy_to_destination):
        src_path, dst_path = 'foo/', 'bar/'
        confirmation = Confirmation.objects.create(src_path=src_path,
                                                   dst_path=dst_path)
        url = reverse('confirm', args=[confirmation.id])
        self.client.get(url)
        copy_to_destination.assert_called_once_with(src_path, dst_path)
