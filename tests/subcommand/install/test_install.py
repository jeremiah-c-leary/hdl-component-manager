
import unittest
from unittest import mock
import logging
import os

from hcm.subcommand.install import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/install/'

def remove_directory(sName):
    try:
        os.rmdir(sName)
    except FileNotFoundError:
        pass


class command_line_args():
    ''' This is used as an input into the install subcommand.'''
    def __init__(self, url=None, component=None, version=None, force=False, external=False):
        self.url = url
        self.component = component
        self.version = version
        self.force = force
        self.external = external
        self.dependencies = False
        self.upgrade = False


class testInstallSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)
      remove_directory('rook')
      remove_directory('queen')
      remove_directory('bishop')

  def tearDown(self):
      logging.disable(logging.NOTSET)
      remove_directory('rook')
      remove_directory('queen')
      remove_directory('bishop')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_install_component_that_exists(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      install(command_line_args('http://svn/my_repo/components', 'rook', '1.0.0', None))
      self.assertTrue(os.path.isdir('rook'))

      install(command_line_args('http://svn/my_repo/components', 'rook', '1.1.0', None))
      self.assertTrue(os.path.isdir('rook'))

      install(command_line_args('http://svn/my_repo/components', 'rook', '2.0.0', None))
      self.assertTrue(os.path.isdir('rook'))

      self.assertFalse(os.path.isdir('queen'))
      install(command_line_args('http://svn/my_repo/components', 'queen', '1.0.0', None))
      self.assertTrue(os.path.isdir('queen'))

      install(command_line_args('http://svn/my_repo/components', 'queen', '2.0.0', None))
      self.assertTrue(os.path.isdir('queen'))

      install(command_line_args('http://svn/my_repo/components', 'queen', '3.0.0', None))
      self.assertTrue(os.path.isdir('queen'))


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_install_component_that_does_not_exist(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      self.assertRaises(SystemExit, install, command_line_args('http://svn/my_repo/components', 'rook', '1.0.1', None))
      self.assertFalse(os.path.isdir('rook'))

      self.assertFalse(os.path.isdir('knight'))
      self.assertRaises(SystemExit, install, command_line_args('http://svn/my_repo/components', 'knight', '1.0.0', None))
      self.assertFalse(os.path.isdir('knight'))

      self.assertFalse(os.path.isdir('queen'))
      self.assertRaises(SystemExit, install, command_line_args('http://svn/my_repo/components', 'queen', '6.0.0', None))
      self.assertFalse(os.path.isdir('queen'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components'})
  def test_install_component_from_url_environment_variable(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      install(command_line_args(None, 'rook', '1.0.0', None))
      self.assertTrue(os.path.isdir('rook'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch.dict('os.environ', {'dummy':'dummy_stuff'}, clear=True)
  def test_install_component_with_no_url(self, mocked_function):

      self.assertFalse(os.path.isdir('rook'))
      self.assertRaises(SystemExit, install, command_line_args(None, 'rook', '1.0.0', None))
      self.assertFalse(os.path.isdir('rook'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'}, clear=True)
  def test_install_component_with_multiple_environment_variables(self, mocked_function):

      self.assertFalse(os.path.isdir('castle'))
      self.assertRaises(SystemExit, install, command_line_args(None, 'castle', '1.0.0', None))
      self.assertFalse(os.path.isdir('castle'))

      self.assertFalse(os.path.isdir('rook'))
      install(command_line_args(None, 'rook', '1.0.0', None))
      self.assertTrue(os.path.isdir('rook'))

      self.assertFalse(os.path.isdir('queen'))
      self.assertRaises(SystemExit, install, command_line_args(None, 'queen', '1.0.0', None))
      self.assertFalse(os.path.isdir('queen'))

      self.assertFalse(os.path.isdir('bishop'))
      install(command_line_args(None, 'bishop', '1.0.0', None))
      self.assertTrue(os.path.isdir('bishop'))

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_is_component_externaled(self, mocked_function):
      self.assertTrue(is_component_externalled('pawn', False))
      self.assertTrue(is_component_externalled('unknown', True))
      self.assertTrue(is_component_externalled('pawn', True))
      self.assertTrue(is_component_externalled('castle', True))
      self.assertFalse(is_component_externalled('rook', False))
      self.assertFalse(is_component_externalled('queen', False))

#  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
#  def test_update_externals(self, mocked_function):
#      self.assertTrue(update_externals('http://svn/external_repo/pawn/10.1.0', 'pawn'), False)
