def install_package(download_path: str):
        pulsar_package = subprocess.run('ppm install download_path', shell = True, capture_output = True, text = True)
    # if(!success) raise Exception("Something went wrong with the installation.")
    pass

def uninstall_package(package_name: str):
    # if(!success) raise Exception("Something went wrong with uninstallation.")
    pass

def get_installed_packages():
    # return [{"package_name": "example_name", "version": "0.0.1"}]
    return []
