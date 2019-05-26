
import unittest
from unittest import mock
import logging
import os

from hcm.subcommand.install import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/install/'


class testInstallSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)
      try:
          os.rmdir('rook')
          os.rmdir('queen')
      except FileNotFoundError:
          pass

  def tearDown(self):
      logging.disable(logging.NOTSET)
      try:
          os.rmdir('rook')
          os.rmdir('queen')
      except FileNotFoundError:
          pass

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_install_component_that_exists(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      install('http://svn/my_repo/components', 'rook', '1.0.0')
      self.assertTrue(os.path.isdir('rook'))

      install('http://svn/my_repo/components', 'rook', '1.1.0')
      self.assertTrue(os.path.isdir('rook'))

      install('http://svn/my_repo/components', 'rook', '2.0.0')
      self.assertTrue(os.path.isdir('rook'))

      self.assertFalse(os.path.isdir('queen'))
      install('http://svn/my_repo/components', 'queen', '1.0.0')
      self.assertTrue(os.path.isdir('queen'))

      install('http://svn/my_repo/components', 'queen', '2.0.0')
      self.assertTrue(os.path.isdir('queen'))

      install('http://svn/my_repo/components', 'queen', '3.0.0')
      self.assertTrue(os.path.isdir('queen'))


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_install_component_that_does_not_exist(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      self.assertRaises(SystemExit, install, 'http://svn/my_repo/components', 'rook', '1.0.1')
      self.assertFalse(os.path.isdir('rook'))

      self.assertFalse(os.path.isdir('knight'))
      self.assertRaises(SystemExit, install, 'http://svn/my_repo/components', 'knight', '1.0.0')
      self.assertFalse(os.path.isdir('knight'))

      self.assertFalse(os.path.isdir('queen'))
      self.assertRaises(SystemExit, install, 'http://svn/my_repo/components', 'queen', '6.0.0')
      self.assertFalse(os.path.isdir('queen'))

