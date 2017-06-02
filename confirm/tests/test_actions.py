from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

from confirm import actions, models


@override_settings(DEFAULT_DST_PATH='/Volumes/dest/')
class RequestConfirm(TestCase):
    def test_creates_confirmation_with_src_path(self):
        actions.request_confirm('./foo')
        confirmation = models.Confirmation.objects.first()
        self.assertEqual(confirmation.src_path, './foo')

    def test_creates_confirmation_with_settings_dst_path_and_basename(self):
        actions.request_confirm('./foo')
        confirmation = models.Confirmation.objects.first()
        self.assertEqual(confirmation.dst_path, '/Volumes/dest/foo')

    @patch('confirm.actions.send_confirm_request')
    def test_creates_confirmation_and_sends(self, send_confirm_request):
        actions.request_confirm('./foo')
        confirmation = models.Confirmation.objects.first()
        send_confirm_request.assert_called_once_with(confirmation)


@patch('confirm.actions.send_email')
class SendConfirmRequestTestCase(TestCase):
    def setUp(self):
        self.confirmation = models.Confirmation.objects.create(
            src_path='foo/', dst_path='bar/')

    def test_calls_send_email_properly(self, send_email_mock):
        actions.send_confirm_request(self.confirmation)

        expected_context = {
            'confirmation': self.confirmation,
        }

        send_email_mock.assert_called_once_with(
            'Affirmative?', actions.EMAIL_ADDRESS,
            [settings.CONFIRMATION_EMAIL], 'confirm_request', expected_context,
            html_to_text=True)


class CopyToDestinationTestCase(TestCase):
    src, dst = 'foo/', 'bar/'

    @patch('confirm.actions.shutil')
    def test_copies_directory_path_to_destination(self, shutil):
        actions.copy_to_destination(self.src, self.dst)
        shutil.copytree.assert_called_once_with(self.src, self.dst)

    @patch('confirm.actions.shutil')
    def test_copies_file_if_not_directory(self, shutil):
        shutil.copytree.side_effect = NotADirectoryError
        actions.copy_to_destination(self.src, self.dst)
        shutil.copy.assert_called_once_with(self.src, self.dst)
