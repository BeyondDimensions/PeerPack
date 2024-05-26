def list_packages():
    # listeing packages
    print("List of packages:")

def install_package(package, version=None, repository=None):
    if version and repository:
        message=(f"Install package: {package}, Version: {version}, from Repository: {repository}")
    elif version:
        message=(f"Install package: {package}, Version: {version}")
    elif repository:
        message=(f"Install package: {package} aus Repository: {repository}")
    else:
        message=(f"Install package: {package}")

    # logic to install packages
    print(message)
    return message

def uninstall_package(package):
    # logic to uninstall
    print(f"Uninstall package: {package}")

def update_package(package):
    # logic to update
    print(f"Update package: {package}")

def version_package(package):
    # logic to check version
    print(f"Version of package: {package}")

def register_package(package, version, repository, description=None):
    # logic to register a package
    print(f"Register package: {package}, Version: {version}, from Repository: {repository}, Description: {description}")
    # Zum Beispiel: In einer Datenbank speichern oder in einer Datei ablegen

def release_package(package, version, file_path, repository):
    # logic to release
    print(f"Release package: {package}, Version: {version}, File: {file_path}, to Repository: {repository}")
    # Datei an ein Repository oder einen Server hochladen
