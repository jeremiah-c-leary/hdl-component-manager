
import unittest
from unittest import mock
import logging
import os

from hcm.subcommand.download import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/download/'

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
      remove_directory('rook_1.0.0')
      remove_directory('rook_1.1.0')
      remove_directory('rook_2.0.0')

  def tearDown(self):
      logging.disable(logging.NOTSET)
      remove_directory('rook_1.0.0')
      remove_directory('rook_1.1.0')
      remove_directory('rook_2.0.0')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'}, clear=True)
  def test_download_component(self, mocked_function):

      self.assertFalse(os.path.isdir('rook_1.0.0'))
      download(command_line_args(component='rook', version='1.0.0'))
      self.assertTrue(os.path.isdir('rook_1.0.0'))

      self.assertFalse(os.path.isdir('rook_1.1.0'))
      download(command_line_args(component='rook', version='1.1.0'))
      self.assertTrue(os.path.isdir('rook_1.1.0'))

      self.assertFalse(os.path.isdir('rook_2.0.0'))
      download(command_line_args(component='rook', version='2.0.0'))
      self.assertTrue(os.path.isdir('rook_2.0.0'))


