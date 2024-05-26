from package_index.pkg_repo import PackageRepo
from installation_management import installation_management


def list_packages():
    pass


def install_package(package, version=None, repository=None):
    installation_management.install(repository, package, version)


def uninstall_package(package):
    installation_management.uninstall(package)


def update_package(package):
    installation_management.uninstall(package)


def get_package_version(package, repository=None):
    PackageRepo(repository).get_package_versions(package)[-1]


def register_package(package, repository, description=None):
    private_key = PackageRepo(repository).register_package(package)
    return private_key


def release_package(package, version, file_path, repository, private_key):
    PackageRepo(repository).release_package(
        package,
        version,
        [],
        file_path,
        private_key
    )
