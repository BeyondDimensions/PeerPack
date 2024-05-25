import unittest
from unittest.mock import patch, MagicMock
import sys
from peerpack import cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('my_package_manager.manager')
        self.mock_manager = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_install_command(self):
        test_args = ['cli.py', 'install', 'myrepo.mypackage', '--version', '1.0.0']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.install_package.assert_called_once_with('mypackage', '1.0.0', 'myrepo')

    def test_register_command(self):
        test_args = ['cli.py', 'register', 'myrepo.mypackage', '--version', '1.0.0', '--description', 'Ein Beispielpaket']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.register_package.assert_called_once_with('mypackage', '1.0.0', 'myrepo', 'Ein Beispielpaket')

    def test_release_command(self):
        test_args = ['cli.py', 'release', 'myrepo.mypackage', '--version', '1.0.0', '--file', '/path/to/package/file.zip']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.release_package.assert_called_once_with('mypackage', '1.0.0', '/path/to/package/file.zip', 'myrepo')

    def test_list_command(self):
        test_args = ['cli.py', 'list']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.list_packages.assert_called_once()

    def test_uninstall_command(self):
        test_args = ['cli.py', 'uninstall', 'mypackage']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.uninstall_package.assert_called_once_with('mypackage')

    def test_update_command(self):
        test_args = ['cli.py', 'update', 'mypackage']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.update_package.assert_called_once_with('mypackage')

    def test_version_command(self):
        test_args = ['cli.py', 'version', 'mypackage']
        with patch.object(sys, 'argv', test_args):
            cli.main()
            self.mock_manager.version_package.assert_called_once_with('mypackage')

if __name__ == '__main__':
    unittest.main()
