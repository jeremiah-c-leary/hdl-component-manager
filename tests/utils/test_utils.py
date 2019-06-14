
import unittest
from unittest import mock

from hcm import utils


class testUtilsMethods(unittest.TestCase):

    def setUp(self):
        self.dExpected = {}
        self.dExpected['publish'] = {}
        self.dExpected['publish']['url'] = 'http://my_repo/components'
        self.dExpected['version'] = '1.0.0'
        self.dExpected['name'] = 'rook'

    def test_get_url(self):
        self.assertEqual(utils.get_url(self.dExpected), 'http://my_repo/components')

    def test_get_version(self):
        self.assertEqual(utils.get_version(self.dExpected), '1.0.0')

    def test_get_component_name(self):
        self.assertEqual(utils.get_component_name(self.dExpected), 'rook')

    def test_get_component_path(self):
        self.assertEqual(utils.get_component_path(self.dExpected), 'http://my_repo/components/rook')

    def test_get_hcm_config_path(self):
        self.assertEqual(utils.get_hcm_config_path(self.dExpected), 'rook/hcm.json')

    def test_get_version_path(self):
        self.assertEqual(utils.get_version_path(self.dExpected), 'http://my_repo/components/rook/1.0.0')


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
        dExpected = {}
        dExpected['requires'] = {}
        dExpected['requires']['queen'] = None
        dExpected['requires']['king'] = None
        dExpected['requires']['castle'] = None

        self.assertEqual(utils.read_dependencies('./bad_directory'), None)
        self.assertEqual(utils.read_dependencies('./tests/utils'), dExpected)
