from django.test import TestCase
from affirmative.settings import utility

from unittest.mock import ANY, patch


class EnvGetOrWarnTestCase(TestCase):
    @patch('affirmative.settings.utility.os')
    def test_when_environment_variable_set_returns(self, os):
        os.environ = {'foo': 'bar'}
        self.assertEqual(utility.env_get_or_warn('foo'), 'bar')

    @patch('affirmative.settings.utility.os')
    @patch('affirmative.settings.utility.log_warning')
    def test_when_environment_variable_not_set_it_logs_warning(self, log, os):
        os.environ = {}
        utility.env_get_or_warn('foo')
        log.assert_called_once_with(ANY, module_name=utility.__name__)

    @patch('affirmative.settings.utility.os')
    @patch('affirmative.settings.utility.log_warning')
    def test_when_environment_variable_not_set_returns_none(self, log, os):
        os.environ = {}
        self.assertIsNone(utility.env_get_or_warn('foo'))


class LogWarningTestCase(TestCase):
    @patch('affirmative.settings.utility.logging')
    def test_gets_logger_properly(self, logging_mock):
        name = 'name'
        utility.log_warning('foo', module_name=name)
        logging_mock.getLogger.assert_called_once_with(name)

    @patch('affirmative.settings.utility.logging')
    def test_logs_warning_with_logger(self, logging_mock):
        utility.log_warning('foo', module_name='name')
        logging_mock.getLogger.return_value.warn.assert_called_once_with('foo')

    def test_not_passing_module_name_raises_error(self):
        with self.assertRaises(TypeError):
            utility.log_warning('foo')
