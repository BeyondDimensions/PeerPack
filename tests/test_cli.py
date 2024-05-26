if True:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from testing_utils import mark
    import testing_utils
    import subprocess
    import dummy_peerpack_api

def test_demo():
    mark(1 == 1, 'Die welt ist noch in Ordnung')

def test_install():
    result = subprocess.run('python3 cli_dummy.py install repo.package', shell = True, capture_output = True, text = True)
    lines = result.stdout.split('\n')
    lines.remove('')
    output=lines[-1]
    expected_output = dummy_peerpack_api.install_package('package', version=None, repository="repo")
    mark(output == expected_output, "install")



def run_tests():
    test_demo()
    test_install()


if __name__ == "__main__":
    testing_utils.RAISE_EXCEPTIONS = False
    run_tests()
