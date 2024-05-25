from utils.logger import logger
from dependency_resolver import resolve
from package_index.pkg_repo import PackageRepo
from native_installer import install_package, uninstall_package, get_installed_packages

def install(repository_name: str, package_name: str, version: str | None = None):
    try:
        logger.info(f"Attempting to resolve dependencies for {package_name}")

        repository = PackageRepo(repository_name)
        # Resolve dependencies
        dependencies = resolve_dependencies(repository, package_name)

        # Retrieve installed packages to avoid reinstallation
        installed_packages = get_installed_packages()

        # Install all dependencies first
        for dep in dependencies:
            if dep not in installed_packages:
                logger.debug(f"Installing dependency {dep}")
                package_path = repository.download_package(dep)
                install_package(package_path)
                logger.info(f"Successfully installed dependency {dep}")

        # Now install the main package if it's not already installed
        if package_name not in installed_packages:
            logger.info(f"Installing main package {package_name}")
            package_path = repository.download_package(package_name, version)
            install_package(package_path)
            logger.info(f"Successfully installed package {package_name}")

    except Exception as e:
        logger.exception(f"An error occurred while installing {package_name}: {e}")


def uninstall(repository_name: str, package_name: str):
    try:
        logger.info(f"Attempting to uninstall {package_name}")

        repository = PackageRepo(repository_name)
        installed_packages = get_installed_packages()

        if package_name in installed_packages:
            uninstall_package(package_name)
            logger.info(f"Successfully uninstalled {package_name}")
        else:
            logger.warning(f"Package {package_name} is not installed.")

    except Exception as e:
        logger.exception(f"An error occurred while uninstalling {package_name}: {e}")


def update(repository_name: str, package_name: str):
    try:
        logger.info(f"Checking for updates for {package_name}")
        repository = PackageRepo(repository_name)
        installed_packages = get_installed_packages()

        if package_name not in installed_packages:
            logger.warning(f"Package {package_name} is not installed. Consider installing it first.")
            return

        current_version = installed_packages[package_name]  # Assuming the version is stored
        latest_version = repository.get_package_versions(package_name)

        if current_version < latest_version:
            logger.info(f"Updating {package_name} from version {current_version} to {latest_version}")
            # Download the package first to ensure it's available before uninstalling
            package_path = repository.download_package(package_name, latest_version)
            # Use existing uninstall and install functions
            uninstall(repository_name, package_name)  # Reuse the existing uninstall functionality
            install(repository_name, package_name, latest_version)  # Reuse the existing install functionality
            logger.info(f"Successfully updated {package_name} to version {latest_version}")
        else:
            logger.info(f"No updates available for {package_name}. Current version: {current_version}")

    except Exception as e:
        logger.exception(f"An error occurred while updating {package_name}: {e}")
