import os
from django.test import TestCase
from django.core import mail

from trigger.tasks import watch_for_new_file

WATCH_DIRECTORY = 'acceptance_tests/tmp/'


def click_affirmative_email_link():
    print(mail.outbox[0].body)


class TriggerTestCase(TestCase):
    def tearDown(self):
        _clean_tmp_folder()

    def test_creating_a_file_in_watch_directory_copies_once_confirmed(self):
        watch_for_new_file(WATCH_DIRECTORY)
        _new_file_at_watch_directory()

        self._assert_affirmative_email_is_sent()
        self.fail()
        click_affirmative_email_link()
        assert_file_exists_in(new_directory)
        assert_file_does_exists_in(directory)

    def _assert_affirmative_email_is_sent(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Affirmative', mail.outbox[0].subject)


def _new_file_at_watch_directory():
    print('***********')
    with open('acceptance_tests/tmp/foobar.txt', 'w') as f:
        f.write('hello world')

    return f


def _clean_tmp_folder():
    folder = 'acceptance_tests/tmp/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.remove(file_path)
