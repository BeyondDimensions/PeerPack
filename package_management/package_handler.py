from dependency_resolver import DependencyResolver
from package_installer import PackageInstaller

class PackageHandler:
    def __init__(self, package_index, package_storage):
        self.resolver = DependencyResolver(package_index)
        self.installer = PackageInstaller(package_storage)

    def handle_package(self, package_name):
        dependencies = self.resolver.resolve(package_name)
        for dep in dependencies:
            self.installer.install(dep)
        self.installer.install(package_name)
