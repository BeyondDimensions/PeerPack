import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import logger

def resolve_dependencies(repository, root_package):
    logger.info(f"Resolving dependencies for {root_package}")
    resolved = set()  # Set to keep track of resolved packages
    unresolved = set()  # Set to detect circular dependencies
    install_order = []  # List to maintain the correct installation order

    def resolve(package_name: str):
        if package_name in resolved:
            return
        if package_name in unresolved:
            raise ValueError(f"Circular dependency detected: {package_name}")

        unresolved.add(package_name)
        latest_version = repository.get_package_versions(package_name)[-1]
        dependencies = repository.get_package_dependencies(package_name, latest_version)

        for dep in dependencies:
            resolve(dep)

        unresolved.remove(package_name)
        resolved.add(package_name)
        install_order.append(package_name)

    try:
        resolve(root_package)
        return install_order
    except ValueError as e:
        print("Error resolving dependencies:", e)
        return None
