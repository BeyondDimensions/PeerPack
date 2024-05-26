from package_index.pkg_repo import PackageRepo


def list_packages():
    pass


def install_package(package, version=None, repository=None):
    pass


def uninstall_package(package):
    pass


def update_package(package):
    pass


def version_package(package):
    pass


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
