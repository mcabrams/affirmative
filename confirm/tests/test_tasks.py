from unittest.mock import patch

from django.test import TestCase

from confirm import tasks


class CopyToDestinationTestCase(TestCase):
    src, dst = 'foo/', 'bar/'

    @patch('confirm.tasks.shutil')
    def test_copies_directory_path_to_destination(self, shutil):
        tasks.copy_to_destination(self.src, self.dst)
        shutil.copytree.assert_called_once_with(self.src, self.dst)

    @patch('confirm.tasks.shutil')
    def test_copies_file_if_not_directory(self, shutil):
        shutil.copytree.side_effect = NotADirectoryError
        tasks.copy_to_destination(self.src, self.dst)
        shutil.copy.assert_called_once_with(self.src, self.dst)
