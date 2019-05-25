
import unittest
from unittest import mock
import subprocess

from hcm import svn
from tests.mocks import mocked_subprocess_check_output


class testSvnMethods(unittest.TestCase):

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_making_new_repo_directory(self, mocked_function):
      self.assertTrue(svn.mkdir('http://svn/my_repo/new_directory'), True)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_attempt_to_make_existing_directory(self, mocked_function):
      self.assertRaises(subprocess.CalledProcessError, svn.mkdir, 'http://svn/my_repo/components')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_if_directory_exists(self, mocked_function):
      self.assertTrue(svn.does_directory_exist('http://svn/my_repo/components/rook'))
      self.assertTrue(svn.does_directory_exist('http://svn/my_repo/components/rook/1.0.0'))
      self.assertFalse(svn.does_directory_exist('http://svn/my_repo/components/rook/1.0.0/a'))
      self.assertTrue(svn.does_directory_exist('http://svn/my_repo/components/queen'))
      self.assertFalse(svn.does_directory_exist('http://svn/my_repo/components/king'))
      self.assertFalse(svn.does_directory_exist('http://svn/my_repo/components/king/1.0.0'))

