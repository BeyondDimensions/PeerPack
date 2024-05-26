import subprocess

def install_package(download_path: str):
    try:
        result = subprocess.run(f'cd {download_path} && ppm install', shell = True, capture_output = True, text = True)
        output = result.stdout.strip()
        error_out = result.stderr.strip()
        return output, error_out, result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, str(e), e.returncode
    pass

def uninstall_package(package_name: str):
    try:
        result = subprocess.run(f'ppm uninstall {package_name}', shell = True, capture_output = True, text = True)
        output = result.stdout.strip()
        error_out = result.stderr.strip()
        return output, error_out, result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, str(e), e.returncode
    pass

def get_installed_packages():
    try:
        result = subprocess.run('ppm view package_name', shell = True, capture_output = True, text = True)
        output = result.stdout.strip()
        error_out = result.stderr.strip()
        return output, error_out, result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, str(e), e.returncode

if __name__ == "__main__":

    print(f"Output:\n{output}")
    print(f"Error:\n{error_out}")
