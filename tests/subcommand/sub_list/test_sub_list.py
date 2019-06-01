
import unittest
from unittest import mock
import logging

from hcm.subcommand.sub_list import *
from tests.mocks import mocked_subprocess_check_output

sTestLocation = 'tests/subcommand/install/'


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



