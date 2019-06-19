
import unittest
from unittest import mock
import logging
import os

from hcm.subcommand.sub_list import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/sub_list/'


class testListSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

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
      sExpected = '--------------------     ----------     -----     ------     ---------'
      dVersions = {}
      dVersions['config'] = {}
      dVersions['config']['max_comp_len'] = 20
      dVersions['config']['max_ver_len'] = 10
      dVersions['config']['max_upgrade_len'] = 5 
      dVersions['config']['max_url_len'] =9 
      self.assertEqual(build_divider(sRow, dVersions), sExpected)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_uncommitted_modifications_status_flag(self, mocked_function):

      self.assertEqual(update_uncommitted_modifications_status_flag('rook'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('queen'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('bishop'), ' ')
      self.assertEqual(update_uncommitted_modifications_status_flag('pawn'), 'U')
      self.assertEqual(update_uncommitted_modifications_status_flag('castle'), 'U')

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_committed_modifications_status_flag(self, mocked_function):

      dVersions = {}
      dVersions['components'] = {}
      dVersions['components']['rook'] = {}
      dVersions['components']['rook']['url'] = 'hello'
      dVersions['components']['queen'] = {}
      dVersions['components']['queen']['url'] = '-----'
      dVersions['components']['pawn'] = {}
      dVersions['components']['pawn']['url'] = 'hello2'
     
      self.assertEqual(update_committed_modifications_status_flag(dVersions, 'rook'), 'M')
      self.assertEqual(update_committed_modifications_status_flag(dVersions, 'queen'), ' ')
      self.assertEqual(update_committed_modifications_status_flag(dVersions, 'pawn'), ' ')


class testGetDirectories(unittest.TestCase):

  def setUp(self):
      os.chdir('tests')

  def tearDown(self):
      os.chdir('..')

  def test_get_directories(self):
      lExpected = ['__pycache__','subcommand', 'svn', 'utils']
      self.assertEqual(get_directories(), lExpected)


#class testInListDirectory(unittest.TestCase):
#
#  def setUp(self):
#      os.chdir('tests/subcommand/sub_list')
#
#  def tearDown(self):
#      os.chdir('../../../')


