from unittest.mock import patch

from django.test import TestCase, override_settings

from confirm.templatetags.utility import url_with_domain


class UrlWithDomainTestCase(TestCase):
    @override_settings(DOMAIN='bar.com')
    @patch('confirm.templatetags.utility.reverse')
    def test_url_accounts_for_domain_set_in_settings(self, reverse):
        actual = url_with_domain('foo')
        self.assertEqual(actual, 'bar.com' + reverse.return_value)

    @patch('confirm.templatetags.utility.reverse')
    def test_reverse_called_with_args(self, reverse):
        url_with_domain('foo', 'bar')
        reverse.assert_called_once_with('foo', args=('bar',), kwargs={})

    @patch('confirm.templatetags.utility.reverse')
    def test_reverse_called_with_kwargs(self, reverse):
        url_with_domain('foo', a='b')
        reverse.assert_called_once_with('foo', kwargs={'a': 'b'}, args=())

    def test_args_and_kwargs_raises_runtime_error(self):
        with self.assertRaises(ValueError):
            url_with_domain('foo', 'bar', a='b')
