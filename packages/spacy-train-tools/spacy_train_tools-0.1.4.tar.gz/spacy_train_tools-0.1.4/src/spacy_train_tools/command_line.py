import logging
import subprocess

from py_profiler import profiler


@profiler('run_command_line')
def run_command_line(command: list):
    logging.info(f'Starting: {command}')
    ps = subprocess.run(command, capture_output=True, check=True, text=True)
    logging.info(ps.stdout.strip())

    logging.info(f'Completed: {command}')
