
import logging
import unittest
from unittest import mock

from hcm import utils


class testUtilsMethods(unittest.TestCase):

    def setUp(self):
        self.dHcmConfig = {}
        self.dHcmConfig['publish'] = {}
        self.dHcmConfig['publish']['url'] = 'http://my_repo/components'
        self.dHcmConfig['version'] = '1.0.0'
        self.dHcmConfig['name'] = 'rook'
        self.dHcmConfig['source'] = {}
        self.dHcmConfig['source']['url'] = 'Source URL'
        self.dHcmConfig['source']['manifest'] = {}
        self.dHcmConfig['source']['manifest']['first'] = '1'
        self.dHcmConfig['source']['manifest']['second'] = '2'
        self.dHcmConfig['source']['manifest']['third'] = '3'
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_url(self):
        self.assertEqual(utils.get_url(self.dHcmConfig), 'http://my_repo/components')

    def test_get_version(self):
        self.assertEqual(utils.get_version(self.dHcmConfig), '1.0.0')

    def test_get_component_name(self):
        self.assertEqual(utils.get_component_name(self.dHcmConfig), 'rook')

    def test_get_component_path(self):
        self.assertEqual(utils.get_component_path(self.dHcmConfig), 'http://my_repo/components/rook')

    def test_get_hcm_config_path(self):
        self.assertEqual(utils.get_hcm_config_path(self.dHcmConfig), 'rook/hcm.json')

    def test_get_version_path(self):
        self.assertEqual(utils.get_version_path(self.dHcmConfig), 'http://my_repo/components/rook/1.0.0')

    @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo'})
    def test_get_url_from_single_environment_variable(self):
        self.assertEqual(utils.get_url_from_environment_variable(), ['http://svn/my_repo'])

    @mock.patch.dict('os.environ', {'dummy':'dummy_stuff'}, clear=True)
    def test_get_url_from_no_environment_variable(self):
        self.assertEqual(utils.get_url_from_environment_variable(), None)

    @mock.patch.dict('os.environ', {'HCM_URL_PATHS':'http://svn/my_repo,http://svn/my_other_repo'})
    def test_get_url_from_multiple_environment_variables(self):
        self.assertEqual(utils.get_url_from_environment_variable(), ['http://svn/my_repo', 'http://svn/my_other_repo'])

    def test_validate_version(self):
        self.assertTrue(utils.validate_version('1.0.0'))
        self.assertFalse(utils.validate_version('1.0'))
        self.assertFalse(utils.validate_version('latest'))
        self.assertTrue(utils.validate_version('234.456.4456'))
        self.assertFalse(utils.validate_version('1'))

    def test_read_dependencies(self):
        dDependencies = {}
        dDependencies['requires'] = {}
        dDependencies['requires']['queen'] = None
        dDependencies['requires']['king'] = None
        dDependencies['requires']['castle'] = None

        self.assertEqual(utils.read_dependencies('./bad_directory'), None)
        self.assertEqual(utils.read_dependencies('./tests/utils'), dDependencies)
        self.assertRaises(SystemExit, utils.read_dependencies, './tests/utils/bad_dependency')

    def test_get_source_url(self):
        self.assertEqual(utils.get_source_url(self.dHcmConfig), 'Source URL')

    def test_get_manifest(self):
        dExpected = {}
        dExpected['first'] = '1'
        dExpected['second'] = '2'
        dExpected['third'] = '3'

        self.assertEqual(utils.get_manifest(self.dHcmConfig), dExpected)
