from django.test import TestCase
from confirm.models import Confirmation


class ConfirmationTestCase(TestCase):
    def test_confirmed_is_false_on_creation(self):
        confirmation = Confirmation.objects.create()
        self.assertFalse(confirmation.confirmed)

    def test_confirm_turns_confirmed_to_true(self):
        confirmation = Confirmation.objects.create()
        confirmation.confirm()
        self.assertTrue(confirmation.confirmed)
