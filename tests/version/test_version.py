import logging
import unittest
from unittest import mock

sTestLocation = 'tests/version/'

from hcm import version

class testUtilsMethods(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_print_version(self):
        self.assertRaises(SystemExit, version.print_version)
