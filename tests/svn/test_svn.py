
import unittest
from unittest import mock
import subprocess

from hcm import svn

class testSvnMethods(unittest.TestCase):

    @mock.patch('subprocess.check_output', mock.create_autospec(subprocess.check_output, return_value='mocked!'))
    def test_mkdir_passing(self):
        self.assertTrue(svn.does_directory_exist('directory'))

    @mock.patch('subprocess.check_output', mock.create_autospec(subprocess.check_output, side_effect=subprocess.CalledProcessError(0, 'hi', 'no')))
    def test_mkdir_failing(self):
        self.assertFalse(svn.does_directory_exist('directory'))

    @mock.patch('subprocess.check_output', mock.create_autospec(subprocess.check_output, return_value='mocked!'))
    def test_mkdir_passing(self):
        self.assertEqual(svn.mkdir('directory'), None)

    @mock.patch('subprocess.check_output', mock.create_autospec(subprocess.check_output, side_effect=subprocess.CalledProcessError(0, 'hi', 'no')))
    def test_mkdir_failing(self):
        self.assertRaises(subprocess.CalledProcessError, svn.mkdir, 'directory')

