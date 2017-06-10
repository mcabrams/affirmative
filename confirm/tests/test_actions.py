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
