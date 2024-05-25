from dependency_resolver import DependencyResolver
from package_installer import PackageInstaller
from package_updater import PackageUpdater
from package_uninstaller import PackageUninstaller

class PackageHandler:
    def __init__(self, package_index, package_storage):
        self.resolver = DependencyResolver(?)
        self.installer = PackageInstaller(?)
        self.updater = PackageUpdater(?)
        self.uninstaller = PackageUninstaller(?)

    def handle_package(self, package_name):
        dependencies = self.resolver.resolve(package_name)
        for dep in dependencies:
            self.installer.install(dep)
        self.installer.install(package_name)
