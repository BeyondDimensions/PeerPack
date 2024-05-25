def resolve_dependencies(repository, root_package):
    logger.info(f"Resolving dependencies for {package_name}")
    resolved = set()  # Set to keep track of resolved packages
    unresolved = set()  # Set to detect circular dependencies
    install_order = []  # List to maintain the correct installation order

    def resolve(package_name: str):
        if package_name in resolved:
            return
        if package_name in unresolved:
            raise ValueError(f"Circular dependency detected: {package_name}")

        unresolved.add(package_name)
        dependencies = repository.get_package_dependencies(package_name, version, min_version, max_version)

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
