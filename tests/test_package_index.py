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
