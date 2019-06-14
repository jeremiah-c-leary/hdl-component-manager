
import unittest
from unittest import mock
import logging
import json
import copy

from hcm.subcommand.publish import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/publish/'


class testExtractUrl(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo'})
  def test_extract_url(self):
      self.assertEqual(extract_url('URL'), 'URL')
      self.assertEqual(extract_url(None), 'http://svn/my_repo')

  @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo,http://svn/my_other_repo'})
  def test_extracting_url_with_multiple_paths_set_in_environment_variable(self):
      self.assertRaises(SystemExit, extract_url, None)


class testReadHcmJsonFile(unittest.TestCase):

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


class testCreateDefaultHcmDictionary(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_default_hcm_dictionary(self):
      dExpected = {}
      dExpected['name'] = 'component'
      dExpected['version'] = '1.0.0'
      dExpected['publish'] = {}
      dExpected['publish']['url'] = 'http://my_url'
      dExpected['source'] = {}
      dExpected['source']['url'] = ''
      dExpected['source']['manifest'] = {}

      self.assertEqual(create_default_hcm_dictionary('component', '1.0.0', 'http://my_url'), dExpected)


class testUpdateSourceUrl(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_update_source_url(self, mocked_function):
      dExpected = {}
      dExpected['publish'] = {}
      dExpected['publish']['url'] = ''
      dExpected['source'] = {}
      dExpected['source']['url'] = ''
      dExpected['name'] = 'rook'
      dExpected['version'] = ''
      dExpected['source']['manifest'] = {}

      dActual = copy.deepcopy(dExpected)
      dExpected['source']['url'] = 'http://svn/my_repo/trunk/project_chess/components/rook@40'

      update_source_url(dActual)
      self.assertEqual(dExpected, dActual)


class testUpdateManifest(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_update_manifest(self):
      dExpected = {}
      dExpected['publish'] = {}
      dExpected['publish']['url'] = ''
      dExpected['source'] = {}
      dExpected['source']['url'] = ''
      dExpected['name'] = sTestLocation + 'rook'
      dExpected['version'] = ''
      dExpected['source']['manifest'] = {}

      dActual = copy.deepcopy(dExpected)
      dExpected['source']['manifest'][sTestLocation + 'rook/lay/filelist.tcl'] = '473fd7ad0333b3d2e1be6b6623cacc82'
      dExpected['source']['manifest'][sTestLocation + 'rook/rtl/rook.vhd'] = '8579704d1db4add11c9d861db3ddaf8d'

      update_manifest(dActual)
      self.assertEqual(dExpected, dActual)


class testUpdateVersion(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_update_version(self):
      dExpected = {}
      dExpected['publish'] = {}
      dExpected['source'] = {}
      dExpected['publish']['url'] = ''
      dExpected['source']['url'] = ''
      dExpected['name'] = sTestLocation + 'rook'
      dExpected['version'] = '1.0.0'
      dExpected['source']['manifest'] = {}

      dActual = copy.deepcopy(dExpected)

      dExpected['version'] = '2.0.0'

      update_version(dActual, '2.0.0')
      self.assertEqual(dExpected, dActual)

      dExpected['version'] = '3.1.2'

      update_version(dActual, '3.1.2')
      self.assertEqual(dExpected, dActual)


class testWriteConfigurationFile(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)
      try:
          os.rename(sTestLocation + 'rook/hcm.json', sTestLocation + 'rook/hcm.json.bak')
      except FileNotFoundError:
          pass

  def tearDown(self):
      logging.disable(logging.NOTSET)
      try:
          os.remove(sTestLocation + 'rook/hcm.json')
          os.rename(sTestLocation + 'rook/hcm.json.bak', sTestLocation + 'rook/hcm.json')
      except FileNotFoundError:
          pass

  def test_write_configuration(self):
      dExpected = {}
      dExpected['publish'] = {}
      dExpected['publish']['url'] = ''
      dExpected['source'] = {}
      dExpected['source']['url'] = ''
      dExpected['name'] = sTestLocation + 'rook'
      dExpected['version'] = '1.0.0'
      dExpected['source']['manifest'] = {}

      write_configuration_file(dExpected)

      with open(sTestLocation + 'rook/hcm.json') as json_file:
          dActual = json.load(json_file)

      self.assertEqual(dExpected, dActual)


class testAddHcmConfigFileToComponentDirectory(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_add_config_file(self, mocked_function):
      '''
      This is not much of a test.
      I do not know a good method to test the output of the svn add command.
      '''
      dExpected = {}
      dExpected['publish'] = {}
      dExpected['publish']['url'] = ''
      dExpected['source'] = {}
      dExpected['source']['source_url'] = ''
      dExpected['name'] = sTestLocation + 'rook'
      dExpected['version'] = '1.0.0'
      dExpected['source']['manifest'] = {}

      self.assertTrue(add_hcm_config_file_to_component_directory(dExpected))


class testCheckIfVersionAlreadyExists(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  @mock.patch('subprocess.check_output', side_effect=mocked_subprocess_check_output)
  def test_if_version_exists(self, mocked_function):

      dExpected = {}
      dExpected['publish'] = {}
      dExpected['publish']['url'] = 'http://svn/my_repo/components'
      dExpected['source'] = {}
      dExpected['source']['url'] = ''
      dExpected['name'] = 'rook'
      dExpected['version'] = '1.0.0'
      dExpected['source']['manifest'] = {}

      self.assertRaises(SystemExit, check_if_version_already_exists, dExpected)

      dExpected['version'] = '7.0.0'
      self.assertFalse(check_if_version_already_exists(dExpected))


class testDoesComponentDirectoryExist(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)
      os.mkdir('.hcm_test')

  def tearDown(self):
      logging.disable(logging.NOTSET)
      os.rmdir('.hcm_test')

  def test_directory_exists(self):

      self.assertRaises(SystemExit, does_component_directory_exist, 'rook')
      self.assertTrue(does_component_directory_exist('.hcm_test'))

