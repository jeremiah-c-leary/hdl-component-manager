
import unittest
import logging

from hcm.subcommand.validate import *

sTestLocation = 'tests/subcommand/validate/'


class testUpdateManifest(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_update_manifest(self):
      dExpected = {}
      dExpected['tests/subcommand/validate/rook/rtl/rook.vhd'] = '6774bc056485054ecdbc3085284952c9'
      dExpected['tests/subcommand/validate/rook/file1.txt'] = '98475036dc73d318982805bf4b16e8b2'

      dActual = generate_manifest(sTestLocation + 'rook')
      self.assertEqual(dExpected, dActual)
