
import unittest
from unittest import mock
import logging

from hcm.subcommand import create
from tests.mocks import mocked_subprocess_check_output


class testCreateSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_creating_directory_that_does_not_exist(self, mocked_function):
      self.assertTrue(create('http://svn/my_repo/new_directory'))
      self.assertTrue(create('http://svn/my_repo/components/knight'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_creating_directory_that_does_exist(self, mocked_function):
      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/rook')
      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/rook/1.0.0')
      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/queen/1.0.0')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_wrong_repo_url(self, mocked_function):
      self.assertRaises(SystemExit, create, 'http://svn/repo/components/knight')



