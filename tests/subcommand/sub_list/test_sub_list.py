
import unittest
from unittest import mock
import logging
import os
import copy

from hcm.subcommand.sub_list import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/sub_list/'


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


class testListSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

      self.dVersions = {}
      self.dVersions['components'] = {}
      self.dVersions['components']['rook'] = {}
      self.dVersions['components']['rook']['url'] = 'hello'
      self.dVersions['components']['rook']['External'] = False
      self.dVersions['components']['rook']['version'] = '1.0.0'
      self.dVersions['components']['rook']['upgrade'] = 'None'
      self.dVersions['components']['queen'] = {}
      self.dVersions['components']['queen']['url'] = '-----'
      self.dVersions['components']['queen']['External'] = False
      self.dVersions['components']['queen']['version'] = '2.0.0'
      self.dVersions['components']['queen']['upgrade'] = '3.0.0'
      self.dVersions['components']['pawn'] = {}
      self.dVersions['components']['pawn']['url'] = 'hello2'
      self.dVersions['components']['pawn']['External'] = True
      self.dVersions['components']['pawn']['version'] = '3.0.0'
      self.dVersions['components']['pawn']['upgrade'] = '3.1.0'
      self.dVersions['config'] = {}
      self.dVersions['config']['max_comp_len'] = 20
      self.dVersions['config']['max_ver_len'] = 10
      self.dVersions['config']['max_upgrade_len'] = 7
      self.dVersions['config']['max_url_len'] = 9

      self.dConfig = {}
      self.dConfig['name'] = 'name'
      self.dConfig['version'] = '1.1.1'
      self.dConfig['publish'] = {}
      self.dConfig['publish']['url'] = 'publish_url'
      self.dConfig['source'] = {}
      self.dConfig['source']['url'] = 'source_url'


  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_get_upgrade(self, mocked_function):

      self.assertEqual(get_upgrade('http://svn/my_repo/components/rook', '1.0.0'), '2.0.0')
      self.assertEqual(get_upgrade('http://svn/my_repo/components/rook', '1.1.0'), '2.0.0')
      self.assertEqual(get_upgrade('http://svn/my_repo/components/rook', '2.0.0'), None)
      self.assertEqual(get_upgrade('http://svn/my_repo/components/queen', '1.0.0'), '3.0.0')
      self.assertEqual(get_upgrade('http://svn/my_repo/components/queen', '2.0.0'), '3.0.0')
      self.assertEqual(get_upgrade('http://svn/my_repo/components/queen', '3.0.0'), None)
      self.assertEqual(get_upgrade('http://svn/external_repo/comps/king', '1.0.0'), '1.1.0')
      self.assertEqual(get_upgrade('http://svn/external_repo/comps/king', '1.1.0'), None)
      self.assertEqual(get_upgrade('http://svn/external_repo/comps/bishop', '1.0.0'), '2.1.0')
      self.assertEqual(get_upgrade('http://svn/external_repo/comps/bishop', '2.0.0'), '2.1.0')
      self.assertEqual(get_upgrade('http://svn/external_repo/comps/bishop', '2.1.0'), None)

  def test_build_row(self):
      sExpected = '{0:20s}     {1:10s}     {2:5s}     {3:6s}     {4:9s}'
      self.assertEqual(build_row(20, 10, 5, 9), sExpected)

  def test_build_divider(self):
      sRow = '{0:20s}     {1:10s}     {2:5s}     {3:6s}     {4:9s}'
      sExpected = '--------------------     ----------     -------     ------     ---------'
      self.assertEqual(build_divider(sRow, self.dVersions), sExpected)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_uncommitted_modifications_status_flag(self, mocked_function):

      self.assertEqual(update_uncommitted_modifications_status_flag('rook'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('queen'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('bishop'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('pawn'), 'U')
      self.assertEqual(update_uncommitted_modifications_status_flag('castle'), 'U')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_committed_modifications_status_flag(self, mocked_function):

      self.assertEqual(update_committed_modifications_status_flag(self.dVersions, 'rook'), 'M')
      self.assertEqual(update_committed_modifications_status_flag(self.dVersions, 'queen'), ' ')
      self.assertEqual(update_committed_modifications_status_flag(self.dVersions, 'pawn'), ' ')

  def test_update_external_status_flag(self):

      self.assertEqual(update_external_status_flag(self.dVersions, 'rook'), ' ')
      self.assertEqual(update_external_status_flag(self.dVersions, 'queen'), ' ')
      self.assertEqual(update_external_status_flag(self.dVersions, 'pawn'), 'E')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_status_field(self, mocked_function):

      self.assertEqual(update_status_field(self.dVersions, 'rook'), ' M ')
      self.assertEqual(update_status_field(self.dVersions, 'queen'), '   ')
      self.assertEqual(update_status_field(self.dVersions, 'pawn'), 'E U')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_versions(self, mockStdout, mockedSubprocess):
      print_versions(self.dVersions)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Component                Version        Upgrade     Status     URL      '),
          mock.call('\n'),
          mock.call('--------------------     ----------     -------     ------     ---------'),
          mock.call('\n'),
          mock.call('pawn                     3.0.0          3.1.0       E U        hello2   '),
          mock.call('\n'),
          mock.call('queen                    2.0.0          3.0.0                  -----    '),
          mock.call('\n'),
          mock.call('rook                     1.0.0          None         M         hello    '),
          mock.call('\n')
      ])

  def test_update_column_width(self):
      dExpected = copy.deepcopy(self.dVersions)
      dExpected['config']['max_comp_len'] = 40

      update_column_width(self.dVersions, 'max_comp_len', 40)
      self.assertEqual(self.dVersions, dExpected)

  def test_copy_url(self):
      dExpected = copy.deepcopy(self.dVersions)
      dExpected['components']['rook']['url'] = 'publish_url'

      copy_url(self.dVersions, self.dConfig, 'rook')
      self.assertEqual(self.dVersions, dExpected, 'rook')

  def test_copy_version(self):
      dExpected = copy.deepcopy(self.dVersions)
      dExpected['components']['rook']['version'] = '1.1.1'

      copy_version(self.dVersions, self.dConfig, 'rook')
      self.assertEqual(self.dVersions, dExpected, 'rook')

  def test_update_external(self):
      lExternals = ['rook', 'queen']
      dExpected = copy.deepcopy(self.dVersions)

      dExpected['components']['rook']['External'] = True
      update_external(self.dVersions, 'rook', lExternals)
      self.assertEqual(self.dVersions, dExpected)

      dExpected['components']['queen']['External'] = True
      update_external(self.dVersions, 'queen', lExternals)
      self.assertEqual(self.dVersions, dExpected)

      dExpected['components']['pawn']['External'] = False
      update_external(self.dVersions, 'pawn', lExternals)
      self.assertEqual(self.dVersions, dExpected)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_parse_externals_into_components(self, mocked_function):
      lExpected = ['castle', 'pawn']
      self.assertEqual(parse_externals_into_components(), lExpected)


class testGetDirectories(unittest.TestCase):

  def setUp(self):
      os.chdir('tests')

  def tearDown(self):
      os.chdir('..')

  def test_get_directories(self):
      lExpected = ['__pycache__','subcommand', 'svn', 'utils', 'version']
      self.assertEqual(get_directories(), lExpected)


class testReadHcmJsonFile(unittest.TestCase):

  def setUp(self):
      os.chdir('tests/subcommand/sub_list')
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      os.chdir('../../../')
      logging.disable(logging.NOTSET)

  def test_read_badly_formatted_hcm_json_file(self):
      self.assertRaises(SystemExit, read_hcm_json_file, '../publish/errored_rook/hcm.json')

  def test_hcm_json_file_w_missing_info(self):
      self.assertRaises(SystemExit, read_hcm_json_file, 'hcm_w_missing_info.json')


class testList(unittest.TestCase):

  def setUp(self):
      os.chdir('tests/subcommand/sub_list')

  def tearDown(self):
      os.chdir('../../../')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_versions(self, mockStdout, mockedSubprocess):
      oCommandLineArguments = command_line_args()
      oCommandLineArguments.all = False

      sub_list(oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Component     Version      Upgrade      Status     URL                          '),
          mock.call('\n'),
          mock.call('---------     --------     --------     ------     -----------------------------'),
          mock.call('\n'),
          mock.call('queen         2.1.0        3.0.0                   http://svn/my_repo/components'),
          mock.call('\n'),
          mock.call('rook          2.0.0        None          M         http://svn/my_repo/components'),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_versions_w_all(self, mockStdout, mockedSubprocess):
      oCommandLineArguments = command_line_args()
      oCommandLineArguments.all = True

      sub_list(oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Component     Version      Upgrade      Status     URL                          '),
          mock.call('\n'),
          mock.call('---------     --------     --------     ------     -----------------------------'),
          mock.call('\n'),
          mock.call('queen         2.1.0        3.0.0                   http://svn/my_repo/components'),
          mock.call('\n'),
          mock.call('rook          2.0.0        None          M         http://svn/my_repo/components'),
          mock.call('\n'),
          mock.call('unknown       -----        -----          U        -----                        '),
          mock.call('\n')
      ])
