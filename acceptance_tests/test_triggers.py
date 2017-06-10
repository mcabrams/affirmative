import os
from base import FunctionalTestCase
from trigger.tasks import watch_for_new_file


SRC_FOLDER = '/Volumes/tmp/src'


class TriggerTestCase(FunctionalTestCase):
    def setUp(self):
        _create_src_directory_if_nonexistent()

    def tearDown(self):
        _clean_tmp_folder()
        # TODO: Add assertion that folder is empty?

    def test_creating_a_file_in_watch_directory_copies_once_confirmed(self):
        watch_for_new_file(SRC_FOLDER)
        _new_file_at_src_directory()
        import time; time.sleep(2)
        self.driver.get(self.url('/confirms'))
        table = self.driver.find_element_by_css_selector('table')
        table.text


def _create_src_directory_if_nonexistent():
    if not os.path.exists(SRC_FOLDER):
        os.makedirs(SRC_FOLDER)


def _new_file_at_src_directory():
    new_file_path = os.path.join(SRC_FOLDER, 'foobar.txt')
    with open(new_file_path, 'w') as f:
        f.write('hello world')

    return f


def _clean_tmp_folder():
    for the_file in os.listdir(SRC_FOLDER):
        file_path = os.path.join(SRC_FOLDER, the_file)
        os.remove(file_path)
