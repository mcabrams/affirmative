import os
import time
from django.test import override_settings
from base import FunctionalTestCase
from trigger.tasks import watch_for_new_file


SRC_FOLDER = '/Volumes/tmp/src'
DST_FOLDER = '/Volumes/tmp/dst'
TEST_FOLDERS = (SRC_FOLDER, DST_FOLDER)


class TriggerTestCase(FunctionalTestCase):
    def setUp(self):
        _create_directories_if_nonexistent()

    def tearDown(self):
        _clean_tmp_folders()
        # TODO: Add assertion that folder is empty?

    def _assertNewFileExistsAtDirectory(self):
        self.assertTrue(os.path.exists('/Volumes/tmp/dst/foobar.txt'))

    @override_settings(DEFAULT_DST_PATH='/Volumes/tmp/dst')
    def test_creating_a_file_in_watch_directory_copies_once_confirmed(self):
        watch_for_new_file(SRC_FOLDER)
        _new_file_at_src_directory()
        time.sleep(1)
        self.driver.get(self.url('/confirms'))
        form_groups = self.driver.find_elements_by_class_name('form-group')
        self.assertEqual(len(form_groups), 1)
        form_group = form_groups[0]
        src_path_sel = '[name="form-0-src_path"]'
        dst_path_sel = '[name="form-0-dst_path"]'
        src_path = form_group.find_element_by_css_selector(src_path_sel)
        dst_path = form_group.find_element_by_css_selector(dst_path_sel)
        self.assertEqual(src_path.get_attribute('value'),
                         '/Volumes/tmp/src/foobar.txt')
        self.assertEqual(dst_path.get_attribute('value'),
                         '/Volumes/tmp/dst/foobar.txt')

        form_group.find_element_by_link_text('Confirm').click()
        time.sleep(1)
        self._assertNewFileExistsAtDirectory()


def _create_directories_if_nonexistent():
    for folder in TEST_FOLDERS:
        _create_directory_if_nonexistent(folder)


def _create_directory_if_nonexistent(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def _new_file_at_src_directory():
    new_file_path = os.path.join(SRC_FOLDER, 'foobar.txt')
    with open(new_file_path, 'w') as f:
        f.write('hello world')

    return f


def _clean_tmp_folders():
    for folder in TEST_FOLDERS:
        _clean_folder(folder)


def _clean_folder(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            os.remove(file_path)
