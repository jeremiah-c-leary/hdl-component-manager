
import unittest
import logging

from hcm.subcommand.validate import *

sTestLocation = 'tests/subcommand/validate/'


class testUpdateManifest(unittest.TestCase):

  def setUp(self):
      logging.disable(logging.CRITICAL)

  def tearDown(self):
      logging.disable(logging.NOTSET)

  def test_generate_manifest(self):
      dExpected = {}
      dExpected['tests/subcommand/validate/rook/rtl/rook.vhd'] = '6774bc056485054ecdbc3085284952c9'
      dExpected['tests/subcommand/validate/rook/file1.txt'] = '98475036dc73d318982805bf4b16e8b2'

      dActual = generate_manifest(sTestLocation + 'rook')
      self.assertEqual(dExpected, dActual)

  def test_add_file_to_manifest(self):
      dManifest = {}

      dExpected = {}

      self.assertFalse(add_file_to_manifest(dManifest, 'hcm.json'), dExpected)
      add_file_to_manifest(dManifest, 'hcm.json')
      self.assertEqual(dManifest, dExpected)
      self.assertFalse(add_file_to_manifest(dManifest, '.svn'), dExpected)
      add_file_to_manifest(dManifest, '.svn')
      self.assertEqual(dManifest, dExpected)

      dExpected['tests/subcommand/validate/rook/file1.txt'] = '98475036dc73d318982805bf4b16e8b2'
      self.assertTrue(add_file_to_manifest(dManifest, sTestLocation + 'rook/file1.txt'), dExpected)
      add_file_to_manifest(dManifest, sTestLocation + 'rook/file1.txt')
      self.assertEqual(dManifest, dExpected)


  def test_validate(self):
      self.assertRaises(SystemExit, validate, sTestLocation + 'bad_rook')
      self.assertEqual(validate(sTestLocation + 'rook'), None)
