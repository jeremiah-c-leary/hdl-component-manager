
import unittest

from hcm import utils

class testUtilsMethods(unittest.TestCase):

    def setUp(self):
        self.dExpected = {}
        self.dExpected['hcm'] = {}
        self.dExpected['hcm']['url'] = 'http://my_repo/components'
        self.dExpected['hcm']['version'] = '1.0.0'
        self.dExpected['hcm']['name'] = 'rook'
        
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
