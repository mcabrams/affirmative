from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from confirm.forms import ConfirmFormset
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
        expected_args = (src_path, dst_path,)
        copy_to_destination.delay.assert_called_once_with(args=expected_args)


class ConfirmsTestCase(TestCase):
    def test_request_returns_200(self):
        url = reverse('confirms')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_renders_confirms_template(self):
        url = reverse('confirms')
        res = self.client.get(url)
        self.assertTemplateUsed(res, 'confirms.html')

    def test_context_passes_model_formset(self):
        url = reverse('confirms')
        res = self.client.get(url)
        self.assertIsInstance(res.context['formset'], ConfirmFormset)
