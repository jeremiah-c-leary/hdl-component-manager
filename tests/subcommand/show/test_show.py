
import unittest
import logging
from unittest import mock
import os

from hcm.subcommand.show import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/show/'

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
        self.manifest = False
        self.upgrades = False
        self.modifications = False


class testUpdateManifest(unittest.TestCase):

  def setUp(self):
      self.oCommandLineArguments = command_line_args(url='http://svn/my_repo/components', component='rook')
      logging.disable(logging.CRITICAL)

#      os.symlink(sTestLocation + 'rook', 'rook')

      self.dHcmJsonFile = {}
      self.dHcmJsonFile['source'] = {}
      self.dHcmJsonFile['source']['manifest'] = {}
      self.dHcmJsonFile['source']['manifest']['file1'] = '123456789'
      self.dHcmJsonFile['source']['manifest']['file2'] = 'abcdef123'
      self.dHcmJsonFile['source']['manifest']['file3'] = '5612ab014'
      self.dHcmJsonFile['name'] = 'rook'
      self.dHcmJsonFile['version'] = '1.0.0'
      self.dHcmJsonFile['publish'] = {}
      self.dHcmJsonFile['publish']['url'] = 'http://svn/my_repo/components'

  def tearDown(self):
      logging.disable(logging.NOTSET)
      try:
          os.unlink('rook')
      except FileNotFoundError:
          pass

  def test_build_row(self):
      sExpected = '{0:20s}     {1:15s}'
      self.assertEqual(sExpected, build_row(20, 15))
      sExpected = '{0:2s}     {1:31s}'
      self.assertEqual(sExpected, build_row(2, 31))

  def test_build_divider(self):
      sExpected = '----  --------'
      sRow = '{0:4s}  {1:8s}'
      self.assertEqual(sExpected, build_divider(sRow, 4, 8))

  @mock.patch('sys.stdout')
  def test_print_manifest(self, mockStdout):

      self.assertEqual(print_manifest(self.oCommandLineArguments, self.dHcmJsonFile), None)
      self.oCommandLineArguments.component = 'rook'
      self.oCommandLineArguments.manifest = True

      print_manifest(self.oCommandLineArguments, self.dHcmJsonFile)
      mockStdout.write.assert_has_calls([
          mock.call('\nManifest'),
          mock.call('\n'),
          mock.call('------------------'),
          mock.call('\n'),
          mock.call('123456789    file1'),
          mock.call('\n'),
          mock.call('abcdef123    file2'),
          mock.call('\n'),
          mock.call('5612ab014    file3'),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_upgrades_w_version_1_0_0(self, mockStdout, mockedSubprocess):

      self.assertEqual(print_upgrades(self.oCommandLineArguments, {}), None)

      self.oCommandLineArguments.upgrades = True
      print_upgrades(self.oCommandLineArguments, self.dHcmJsonFile)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Available Upgrades'),
          mock.call('\n'),
          mock.call('=================='),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Version: 2.0.0'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('r10 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('initial release'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Version: 1.1.0'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('r10 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('initial release'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_upgrades_w_version_1_1_0(self, mockStdout, mockedSubprocess):

      self.assertEqual(print_upgrades(self.oCommandLineArguments, {}), None)

      self.oCommandLineArguments.upgrades = True
      self.dHcmJsonFile['version'] = '1.1.0'

      print_upgrades(self.oCommandLineArguments, self.dHcmJsonFile)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Available Upgrades'),
          mock.call('\n'),
          mock.call('=================='),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Version: 2.0.0'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('r10 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('initial release'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n')
      ])


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_upgrades_w_version_2_0_0(self, mockStdout, mockedSubprocess):

      self.assertEqual(print_upgrades(self.oCommandLineArguments, {}), None)

      self.oCommandLineArguments.upgrades = True
      self.dHcmJsonFile['version'] = '2.0.0'

      print_upgrades(self.oCommandLineArguments, self.dHcmJsonFile)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Available Upgrades'),
          mock.call('\n'),
          mock.call('=================='),
          mock.call('\n'),
          mock.call('No Upgrades'),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_show_without_dependencies(self, mockStdout, mockedSubprocess):

      os.symlink(sTestLocation + 'rook', 'rook')

      show(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call('------------     ------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('Component        rook                                                                    '),
          mock.call('\n'),
          mock.call('Version          4.0.0                                                                   '),
          mock.call('\n'),
          mock.call('URL              file:///home/jeremiah/svn/my_repo/comps                                 '),
          mock.call('\n'),
          mock.call('Source           file:///home/jeremiah/svn/my_repo/trunk/project_chess/components/rook@41'),
          mock.call('\n'),
          mock.call('Dependencies     No dependencies found                                                   '),
          mock.call('\n'),
          mock.call('------------     ------------------------------------------------------------------------'),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_show_with_dependencies(self, mockStdout, mockedSubprocess):

      os.symlink(sTestLocation + 'rook_with_deps', 'rook')

      show(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call('------------     ------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('Component        rook                                                                    '),
          mock.call('\n'),
          mock.call('Version          4.0.0                                                                   '),
          mock.call('\n'),
          mock.call('URL              file:///home/jeremiah/svn/my_repo/comps                                 '),
          mock.call('\n'),
          mock.call('Source           file:///home/jeremiah/svn/my_repo/trunk/project_chess/components/rook@41'),
          mock.call('\n'),
          mock.call('Dependencies     king, queen, castle                                                     '),
          mock.call('\n'),
          mock.call('------------     ------------------------------------------------------------------------'),
          mock.call('\n')
      ])

  def test_show_with_invalid_directory(self):

      self.assertRaises(SystemExit, show, self.oCommandLineArguments)


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_committed_modifications(self, mockStdout, mockedSubprocess):

      self.oCommandLineArguments.component = 'rook'
      self.oCommandLineArguments.modifications = True

      print_committed_modifications(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Committed Modifications'),
          mock.call('\n'),
          mock.call('======================='),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n'),
          mock.call('r11 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('initial release'),
          mock.call('\n'),
          mock.call('------------------------------------------------------------------------'),
          mock.call('\n')
      ])


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_no_committed_modifications(self, mockStdout, mockedSubprocess):

      self.oCommandLineArguments.component = 'queen'
      self.oCommandLineArguments.modifications = True

      print_committed_modifications(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Committed Modifications'),
          mock.call('\n'),
          mock.call('======================='),
          mock.call('\n'),
          mock.call('No Committed Modifications')
      ])


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_uncommitted_modifications(self, mockStdout, mockedSubprocess):

      self.oCommandLineArguments.component = 'castle'
      self.oCommandLineArguments.modifications = True

      print_uncommitted_modifications(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Uncommitted Modifications'),
          mock.call('\n'),
          mock.call('========================='),
          mock.call('\n'),
          mock.call('A  +    castle'),
          mock.call('\n'),
          mock.call('?       castle/rtl/movement.vhd'),
          mock.call('\n'),
          mock.call('M  +    castle/rtl/castle-rtl.vhd'),
          mock.call('\n')
      ])


  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_no_uncommitted_modifications(self, mockStdout, mockedSubprocess):

      self.oCommandLineArguments.component = 'queen'
      self.oCommandLineArguments.modifications = True

      print_uncommitted_modifications(self.oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Uncommitted Modifications'),
          mock.call('\n'),
          mock.call('========================='),
          mock.call('\n'),
          mock.call('No Uncommitted Modifications')
      ])

