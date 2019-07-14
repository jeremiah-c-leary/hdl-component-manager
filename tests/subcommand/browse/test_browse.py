
import unittest
from unittest import mock
import logging

from hcm.subcommand.browse import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/browse/'


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


class testBrowseSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)


  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'})
  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_get_components(self, mocked_function):
      lExpected = [['bishop', 'http://svn/external_repo/comps'], ['king', 'http://svn/external_repo/comps'], ['pawwn', 'http://svn/my_repo/components'], ['queen', 'http://svn/external_repo/comps'], ['queen', 'http://svn/my_repo/components'], ['rook', 'http://svn/my_repo/components']]
      self.assertEqual(lExpected, get_components(utils.get_url_from_environment_variable()))

  def test_get_maximum_component_length(self):
      lTest = [['one', 'aaa'], ['two', 'bbb'], ['three', 'ccc']]
      self.assertEqual(9, get_maximum_component_length(lTest))
      lTest.append(['reallylongname', 'ddd'])
      self.assertEqual(14, get_maximum_component_length(lTest))

  def test_get_maximum_url_length(self):
      lTest = [['one', 'aaa'], ['two', 'bbb'], ['three', 'cccccc']]
      self.assertEqual(6, get_maximum_url_length(lTest))

  def test_build_row(self):
      sExpected = '{0:20s}     {1:10s}     {2:9s}'
      self.assertEqual(build_row(20, 10, 9), sExpected)

  def test_build_divider(self):
      sRow = '{0:20s}     {1:10s}     {2:9s}'
      sExpected = '--------------------     ----------     ---------'
      self.assertEqual(build_divider(sRow, 20, 10, 9), sExpected)

  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'})
  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_print_components(self, mockStdout, mocked_function):
      lComponents = get_components(utils.get_url_from_environment_variable())
      print_components(lComponents)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Component     Version      URL                           '),
          mock.call('\n'),
          mock.call('---------     --------     ------------------------------'),
          mock.call('\n'),
          mock.call('bishop        2.1.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('king          1.1.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('pawwn         None         http://svn/my_repo/components '),
          mock.call('\n'),
          mock.call('queen         3.0.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('queen         3.0.0        http://svn/my_repo/components '),
          mock.call('\n'),
          mock.call('rook          2.0.0        http://svn/my_repo/components '),
          mock.call('\n')
      ])

  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'})
  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_browse(self, mockStdout, mocked_function):
      oCommandLineArguments = command_line_args()
      browse(oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Component     Version      URL                           '),
          mock.call('\n'),
          mock.call('---------     --------     ------------------------------'),
          mock.call('\n'),
          mock.call('bishop        2.1.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('king          1.1.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('pawwn         None         http://svn/my_repo/components '),
          mock.call('\n'),
          mock.call('queen         3.0.0        http://svn/external_repo/comps'),
          mock.call('\n'),
          mock.call('queen         3.0.0        http://svn/my_repo/components '),
          mock.call('\n'),
          mock.call('rook          2.0.0        http://svn/my_repo/components '),
          mock.call('\n')
      ])

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_browse_w_out_environment_variable(self, mockStdout, mocked_function):
      oCommandLineArguments = command_line_args(component='rook')
      self.assertRaises(SystemExit, browse, oCommandLineArguments)


  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo/components,http://svn/external_repo/comps'})
  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  @mock.patch('sys.stdout')
  def test_browse_w_component(self, mockStdout, mocked_function):
      oCommandLineArguments = command_line_args(component='rook')
      browse(oCommandLineArguments)
      mockStdout.write.assert_has_calls([
          mock.call('rook versions available:'),
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
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Version: 1.0.0'),
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
          mock.call('\n')
      ])
