def resolve(package_name, version):
    logger.info(f"Resolving dependencies for {package_name}")
    dependencies = get_package_dependencies(package_name, version)
    for dep in dependencies:
        resolve(dep.package_name)
    pass
