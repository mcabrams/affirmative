from watchdog.events import FileSystemEventHandler
from unittest.mock import MagicMock, call, patch
from django.test import TestCase

from trigger import tasks

PATH = 'foo/bar/'


class WatchDirectoryTestCase(TestCase):
    @patch('trigger.tasks.Observer')
    def test_watch_directory_instantiates_observer(self, Observer):
        handler = MagicMock()
        tasks.watch_directory(handler, PATH)
        Observer.assert_called_once_with()

    @patch('trigger.tasks.Observer')
    def test_watch_directory_schedules_then_starts_observer(self, Observer):
        handler = MagicMock()
        tasks.watch_directory(handler, PATH)
        expected_calls = [call.schedule(handler, PATH), call.start()]
        self.assertEqual(Observer().mock_calls, expected_calls)


class NewFileHandlerTestCase(TestCase):
    def test_is_instance_of_file_system_event_handler(self):
        handler = tasks.NewFileHandler()
        self.assertIsInstance(handler, FileSystemEventHandler)

    @patch('trigger.tasks.request_confirm')
    def test_calls_request_confirm_on_created(self, request_confirm):
        event = MagicMock()
        handler = tasks.NewFileHandler()
        handler.on_created(event)
        request_confirm.assert_called_once_with(event.src_path)


class WatchForNewFileTestCase(TestCase):
    @patch('trigger.tasks.NewFileHandler')
    @patch('trigger.tasks.watch_directory')
    def test_calls_watch_directory(self, watch_dir, NewFileHandler):
        path = 'foo'
        tasks.watch_for_new_file(path)
        watch_dir.assert_called_once_with(NewFileHandler.return_value, path)
