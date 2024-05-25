from utils.logger import logger
from dependency_resolver import resolve
from package_index.pkg_repo import PackageRepo
from native_installer import install_package, uninstall_package, get_installed_packages

class InstallationManagement:
    def __init__(self, repository_name):
        self.repository = PackageRepo(repository_name)

def install(repository_name: str, package_name: str, version: str | None):
    logger.info(f"Installing package {package_name}")
    dependencies = resolver.resolve(package_name)
    for dep in dependencies:
        logger.debug(f"Installing dependency {dep}")
        installer.install(dep)
    try:
        logger.debug(f"Starting installation of {package_name}")
        path = self.repository.download_package(package_name, version)
        install_package(path)
        logger.info(f"Successfully installed package {package_name}")
    except Exception as e:
        logger.exception(f"An error occurred while installing package {package_name}: {e}")

def uninstall(package_name):
    # Logic to install the given package
    pass

def update(package_name):
    logger.info(f"Updating package {package_name}")
    # Logic to update the package: uninstall and then install the new version
    self.uninstaller.uninstall(package_name)
    self.installer.install(package_name)
    logger.info(f"Successfully updated package {package_name}")


def install(package, version=None):
    installer = PackageInstaller(package_storage)
    resolver = DependencyResolver(package_index)
    dependencies = resolver.resolve(package_name)
    for dep in dependencies:
        logger.debug(f"Installing dependency {dep}")
        installer.install(dep)
def uninstall (package):
    uninstaller = PackageUninstaller(package_storage)
    uninstaller.uninstall(package_name)
def update(package):
    updater = PackageUpdater(package_storage)
    updater.update(package_name)
