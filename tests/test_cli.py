import sys
import os
import testing_utils
import dummy_peerpack_api

if True:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from testing_utils import mark
    from utils.shell_tools import run_shell_command


def test_install():
    output = run_shell_command("python3 cli_dummy.py install repo.package")[-1]
    expected_output = dummy_peerpack_api.install_package('package', version=None, repository="repo")
    mark(output == expected_output, "install")


def run_tests():
    test_install()


if __name__ == "__main__":
    testing_utils.RAISE_EXCEPTIONS = False
    run_tests()
