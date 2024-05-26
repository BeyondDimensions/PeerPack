import subprocess

download_path = '/Users/marvinkirsch/MockRepository/atom-clock-master'

def install_package(download_path: str):
    try:
        result = subprocess.run(f'cd {download_path} && ppm install', shell = True, capture_output = True, text = True)
        output = result.stdout.strip()
        error_out = result.stderr.strip()
        return output, error_out, result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, str(e), e.returncode

if __name__ == "__main__":
    output, error_out, returncode = install_package(download_path)
    print(f"Output:\n{output}")
    print(f"Error:\n{error_out}")
