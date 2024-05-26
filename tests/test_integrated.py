import subprocess
import tempfile
import sys
import os
if True:
    PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(PROJECT_DIR)
    os.chdir(PROJECT_DIR)
    from package_index.create_repo import create_repo
    from package_index.pkg_repo import PackageRepo
    from testing_utils import mark
    import testing_utils
    from utils.shell_tools import run_shell_command
import walytis_beta_api as wapi
REPO_NAME = "test_repo"
BLOCKCHAIN_NAME = f"PeerPack-{REPO_NAME}"

package_repo: PackageRepo
private_key: str

PACKAGE_NAME = "test_package"
PACKAGE_DATA = "./"


def test_preparations():
    if BLOCKCHAIN_NAME in wapi.list_blockchain_names():
        wapi.delete_blockchain(BLOCKCHAIN_NAME)
    create_repo(REPO_NAME)
    global package_repo
    package_repo = PackageRepo(REPO_NAME)


def test_register_package():
    global private_key
    private_key = run_shell_command(
        f"python3 cli.py register {REPO_NAME}.{PACKAGE_NAME}"
    )[-1]
    mark(PACKAGE_NAME in package_repo.list_packages(), "Registered package.")


def test_release_package():
    global private_key
    version = "1.0.1"
    file = clone_github_repo("https://github.com/donovanhiland/atom-file-icons")
    file = clone_github_repo("https://github.com/b3by/atom-clock")

    run_shell_command(
        f"python3 cli.py release {REPO_NAME}.{PACKAGE_NAME} --version {version} --file {file} --key {private_key}"
    )

    mark(package_repo.get_package_versions(PACKAGE_NAME) == [version], "Released package.")


def test_get_version():
    output = run_shell_command(
        f"python3 cli.py version {REPO_NAME}.{PACKAGE_NAME}"
    )[-1]
    mark(output == "1.0.0")


def clone_github_repo(repo_url):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Run the git clone command in the temporary directory
    subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)

    # Return the path to the temporary directory
    return temp_dir


def test_install_package():
    global private_key
    version = "1.0.1"
    os.system(
        f"python3 cli.py install {REPO_NAME}.{PACKAGE_NAME} --version {version}"
    )

    mark(package_repo.get_package_versions(PACKAGE_NAME) == [version], "Released package.")


def test_delete_repo():
    package_repo.delete()
    mark(BLOCKCHAIN_NAME not in wapi.list_blockchain_names(), "Deleted repo.")


def run_tests():
    test_preparations()
    test_register_package()
    test_release_package()
    test_install_package()
    test_delete_repo()


if __name__ == "__main__":
    testing_utils.RAISE_EXCEPTIONS = False
    run_tests()
