import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from installation_management.native_installer import install_package, uninstall_package, get_installed_packages
from installation_management.installation_management import install, uninstall, update
from installation_management.dependency_resolver import resolve_dependencies
from package_index.create_repo import create_repo
from package_index.pkg_repo import PackageRepo
from testing_utils import mark
import testing_utils
import walytis_beta_api as wapi
REPO_NAME = "test_repo"
BLOCKCHAIN_NAME = f"PeerPack-{REPO_NAME}"
package_name = "xyz"
package_repo: PackageRepo

#
# # Mock classes and functions
# class MockPackageRepo:
#     def __init__(self, repository_name):
#         self.repository_name = repository_name
#
#     def download_package(self, package_name, version=None):
#         return f'/path/to/{package_name}-{version}.tar.gz'
#
#     def get_package_versions(self, package_name):
#         return ['2.0.0', '1.0.0', '1.2.4']
#
#
# PackageRepo = MockPackageRepo

def test_preparations():
    if BLOCKCHAIN_NAME in wapi.list_blockchain_names():
        wapi.delete_blockchain(BLOCKCHAIN_NAME)
    global package_repo
    create_repo(REPO_NAME)
    repo = PackageRepo(REPO_NAME)
    pk = repo.register_package(package_name)
    repo.release_package(package_name, "0.0.1", [], "./", pk)
    mark(repo, "Released package.")


def test_install():
    # Call the function
    install(REPO_NAME, package_name)

    # Check the outputs (here we simply print to verify, in a real test we would use assertions)
    print("Install test completed.")

def test_uninstall():
    # Call the function
    uninstall(REPO_NAME, package_name)

    # Check the outputs (here we simply print to verify, in a real test we would use assertions)
    print("Uninstall test completed.")

def test_update():
    # Call the function
    update(REPO_NAME, package_name)

    # Check the outputs (here we simply print to verify, in a real test we would use assertions)
    print("Update test completed.")


if __name__ == '__main__':
    test_preparations()
    test_install()
    test_uninstall()
    test_update()
