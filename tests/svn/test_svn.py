
import unittest
from unittest import mock
import subprocess
import logging
import os

from hcm import svn
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/svn/'


class testSvnMethods(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)
      try:
          os.rmdir(sTestLocation + 'rook')
      except FileNotFoundError:
          pass

  def tearDown(self):
      logging.disable(logging.NOTSET)
      try:
          os.rmdir(sTestLocation + 'rook')
      except FileNotFoundError:
          pass

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

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_copy(self, mocked_function):

      self.assertFalse(os.path.isdir(sTestLocation + 'rook'))
      svn.copy('http://svn/my_repo/components/rook/1.0.0', sTestLocation + 'rook')
      self.assertTrue(os.path.isdir(sTestLocation + 'rook'))

      self.assertFalse(os.path.isdir(sTestLocation + 'bishop'))
      self.assertRaises(subprocess.CalledProcessError, svn.copy, 'http://svn/my_repo/components/bishop/1.0.1', sTestLocation + 'bishop')
      self.assertFalse(os.path.isdir(sTestLocation + 'bishop'))

      self.assertRaises(subprocess.CalledProcessError, svn.copy, 'rook', 'http://svn/my_repo/components/rook/1.0.0')
      self.assertTrue(svn.copy('rook', 'http://svn/my_repo/components/rook/4.0.0'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_extract_path_url(self, mocked_function):
      self.assertEqual(svn.extract_root_url_from_directory('.'), 'http://svn/my_repo')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_export(self, mocked_function):

      self.assertFalse(os.path.isdir(sTestLocation + 'rook'))
      svn.export('http://svn/my_repo/components/rook/1.0.0', sTestLocation + 'rook')
      self.assertTrue(os.path.isdir(sTestLocation + 'rook'))

      self.assertFalse(os.path.isdir(sTestLocation + 'bishop'))
      self.assertRaises(subprocess.CalledProcessError, svn.export, 'http://svn/my_repo/components/bishop/1.0.1', sTestLocation + 'bishop')
      self.assertFalse(os.path.isdir(sTestLocation + 'bishop'))

      self.assertRaises(subprocess.CalledProcessError, svn.export, 'rook', 'http://svn/my_repo/components/rook/1.0.0')
      self.assertTrue(svn.export('rook', 'http://svn/my_repo/components/rook/4.0.0'))


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_svn_get_externals(self, mocked_function):

      sExpected = "http://svn/external_repo/blocks/castle/1.0.0 castle\n"
      sExpected += "http://svn/external_repo/blocks/pawn/3.0.0 pawn\n"

      self.assertEqual(svn.get_externals('.'), sExpected)
      self.assertEqual(svn.get_externals('fail'), None)


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_directory_has_committed_modifications(self, mocked_component):
      self.assertFalse(svn.directory_has_committed_modifications('pawn'))
      self.assertTrue(svn.directory_has_committed_modifications('rook'))
