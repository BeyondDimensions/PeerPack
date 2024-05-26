import subprocess
from utils.logger import logger


def run_shell_command(command: str) -> list[str]:
    """Run a shell command.

    Returns:
        list[str]: the lines printed to the standard output
    """
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    if result.stderr:
        logger.error(result.stderr)
        raise Exception("Executing shell command failed.")
    lines = result.stdout.split('\n')

    lines.remove('')
    return lines
