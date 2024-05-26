if True:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from package_index.create_repo import create_repo
    from package_index.pkg_repo import PackageRepo
    from testing_utils import mark
    import testing_utils
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


def test_create_repo():
    global package_repo
    create_repo(REPO_NAME)
    package_repo = PackageRepo(REPO_NAME)
    mark(package_repo.blockchain.name == BLOCKCHAIN_NAME, "Created Repo.")


def test_register_package():
    global private_key
    private_key = package_repo.register_package(PACKAGE_NAME)
    mark(PACKAGE_NAME in package_repo.list_packages(), "Registered package.")


def test_release_package():
    package_repo.release_package(
        PACKAGE_NAME,
        "0.0.1",
        [],
        PACKAGE_DATA,
        private_key
    )
    mark(package_repo, "Released package.")


def test_delete_repo():
    package_repo.delete()
    mark(BLOCKCHAIN_NAME not in wapi.list_blockchain_names(), "Deleted repo.")


def run_tests():
    test_preparations()
    test_create_repo()
    test_register_package()
    test_release_package()
    test_delete_repo()


if __name__ == "__main__":
    testing_utils.RAISE_EXCEPTIONS = False
    run_tests()
