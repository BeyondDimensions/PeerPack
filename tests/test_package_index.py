if True:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from package_index.create_repo import create_repo
    from package_index.pkg_repo import PackageRepo

REPO_NAME = "test_repo"

package_repo: PackageRepo


def test_create_repo():
    global package_repo
    create_repo(REPO_NAME)
    package_repo = PackageRepo(REPO_NAME)


def test_delete_repo():
    package_repo.delete()


def run_tests():
    test_create_repo()
    test_delete_repo()


if __name__ == "__main__":
    run_tests()
