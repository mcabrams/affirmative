from django import forms
from django.test import TestCase

from confirm import models
from confirm.forms import ConfirmFormset


class ConfirmFormsetTestCase(TestCase):
    def test_confirm_formset_uses_text_input_for_paths(self):
        models.Confirmation.objects.create()
        expected_widget = forms.TextInput
        for field in ('src_path', 'dst_path',):
            actual = ConfirmFormset().forms[0].fields[field].widget
            self.assertIsInstance(actual, expected_widget)
