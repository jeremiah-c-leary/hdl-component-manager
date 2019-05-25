
import unittest
from unittest import mock
import logging
import json

from hcm.subcommand.publish import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/publish/'

class testPublishSubcommand(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_reading_json_file(self):
      with open(sTestLocation + 'rook/hcm.json') as json_file:
          dRookExpected = json.load(json_file)

      self.assertEqual(read_hcm_json_file(sTestLocation + 'knight'), None)
      self.assertEqual(read_hcm_json_file(sTestLocation + 'rook'), dRookExpected)
      self.assertEqual(read_hcm_json_file(sTestLocation + 'errored_rook'), None)

  def test_default_hcm_dictionary(self):
      dExpected = {}
      dExpected['hcm'] = {}
      dExpected['hcm']['url'] = 'http://my_url'
      dExpected['hcm']['source_url'] = ''
      dExpected['hcm']['name'] = 'component'
      dExpected['hcm']['version'] = '1.0.0'
      dExpected['hcm']['manifest'] = {}

      self.assertEqual(create_default_hcm_dictionary('component', '1.0.0', 'http://my_url'), dExpected)

#  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
#  def test_creating_directory_that_does_not_exist(self, mocked_function):
#      self.assertTrue(create('http://svn/my_repo/new_directory'))
#      self.assertTrue(create('http://svn/my_repo/components/knight'))
#
#  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
#  def test_creating_directory_that_does_exist(self, mocked_function):
#      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/rook')
#      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/rook/1.0.0')
#      self.assertRaises(SystemExit, create, 'http://svn/my_repo/components/queen/1.0.0')
#
#  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
#  def test_wrong_repo_url(self, mocked_function):
#      self.assertRaises(SystemExit, create, 'http://svn/repo/components/knight')



