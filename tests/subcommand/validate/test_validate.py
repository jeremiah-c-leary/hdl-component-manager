
import unittest
from unittest import mock
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

  def test_check_for_missing_files(self):
      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook_w_missing_file')
      dRealManifest = generate_manifest(sTestLocation + 'rook_w_missing_file')
      self.assertEqual(check_for_missing_files(dHcmJsonFile, dRealManifest), [sTestLocation + 'rook_w_missing_file/' + 'file1.txt'])

      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook')
      dRealManifest = generate_manifest(sTestLocation + 'rook')
      self.assertEqual(check_for_missing_files(dHcmJsonFile, dRealManifest), [])

      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook_w_missing_extra_differing_md5sums')
      dRealManifest = generate_manifest(sTestLocation + 'rook_w_missing_extra_differing_md5sums')
      self.assertEqual(check_for_missing_files(dHcmJsonFile, dRealManifest), [sTestLocation + 'rook_w_missing_extra_differing_md5sums/' + 'file1.txt'])


  def test_check_for_extra_files(self):
      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook_w_extra_file')
      dRealManifest = generate_manifest(sTestLocation + 'rook_w_extra_file')
      self.assertEqual(check_for_extra_files(dHcmJsonFile, dRealManifest), [sTestLocation + 'rook_w_extra_file/rtl/rook-arch.vhd'])

      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook')
      dRealManifest = generate_manifest(sTestLocation + 'rook')
      self.assertEqual(check_for_extra_files(dHcmJsonFile, dRealManifest), [])

  def test_check_for_changed_files(self):
      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook_w_differing_md5sums')
      dRealManifest = generate_manifest(sTestLocation + 'rook_w_differing_md5sums')
      self.assertEqual(check_for_changed_files(dHcmJsonFile, dRealManifest), [sTestLocation + 'rook_w_differing_md5sums/rtl/rook.vhd'])

      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook')
      dRealManifest = generate_manifest(sTestLocation + 'rook')
      self.assertEqual(check_for_changed_files(dHcmJsonFile, dRealManifest), [])

      dHcmJsonFile = utils.read_hcm_json_file(sTestLocation + 'rook_w_missing_extra_differing_md5sums')
      dRealManifest = generate_manifest(sTestLocation + 'rook_w_missing_extra_differing_md5sums')
      self.assertEqual(check_for_changed_files(dHcmJsonFile, dRealManifest), [sTestLocation + 'rook_w_missing_extra_differing_md5sums/rtl/rook.vhd'])


  def test_validate(self):
      self.assertRaises(SystemExit, validate, sTestLocation + 'bad_rook', False)
      self.assertEqual(validate(sTestLocation + 'rook', False), None)

  @mock.patch('sys.stdout')
  def test_validate_w_reporting(self, mockStdout):
      validate(sTestLocation + 'rook_w_missing_extra_differing_md5sums', True)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Missing Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_missing_extra_differing_md5sums/file1.txt'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Extra Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_missing_extra_differing_md5sums/rtl/rook-arch.vhd'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Changed Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_missing_extra_differing_md5sums/rtl/rook.vhd'),
          mock.call('\n')
      ])

  @mock.patch('sys.stdout')
  def test_validate_w_reporting_on_missing_file(self, mockStdout):
      validate(sTestLocation + 'rook_w_missing_file', True)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Missing Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_missing_file/file1.txt'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Extra Files'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Changed Files'),
          mock.call('\n')
      ])

  @mock.patch('sys.stdout')
  def test_validate_w_reporting_on_extra_file(self, mockStdout):
      validate(sTestLocation + 'rook_w_extra_file', True)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Missing Files'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Extra Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_extra_file/rtl/rook-arch.vhd'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Changed Files'),
          mock.call('\n')
      ])

  @mock.patch('sys.stdout')
  def test_validate_w_reporting_differing_md5sums(self, mockStdout):
      validate(sTestLocation + 'rook_w_differing_md5sums', True)
      mockStdout.write.assert_has_calls([
          mock.call(''),
          mock.call('\n'),
          mock.call('Missing Files'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Extra Files'),
          mock.call('\n'),
          mock.call(''),
          mock.call('\n'),
          mock.call('Changed Files'),
          mock.call('\n'),
          mock.call('  tests/subcommand/validate/rook_w_differing_md5sums/rtl/rook.vhd'),
          mock.call('\n')
      ])

