
import unittest
from unittest import mock
import subprocess
import logging

from hcm import svn
from tests.mocks import mocked_subprocess_check_output


class testSvnMethods(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

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

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_wrong_repo_url(self, mocked_function):
      self.assertRaises(subprocess.CalledProcessError, svn.mkdir, 'http://svn/repo/components')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_status_is_clean(self, mocked_function):

      self.assertRaises(SystemExit, svn.is_directory_status_clean, 'knight')
      self.assertTrue(svn.is_directory_status_clean('rook'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_delete(self, mocked_function):

      self.assertTrue(svn.delete('rook'))
      self.assertRaises(subprocess.CalledProcessError, svn.delete, 'knight')

