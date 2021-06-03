from sys import stdout
from logging import Logger, Formatter, StreamHandler, DEBUG
from logging.handlers import TimedRotatingFileHandler
from modules.config import Config
from pathlib import Path

FORMATTER = Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
LOG_DIR = Config.get('Logs', 'LogDir')
Path(LOG_DIR).mkdir(exist_ok=True)


class AppLogger(Logger):
    """
        Class to provide custom logging format
        Allow to log in different files.
        Files names are determined with the name passed to the get_logger function
    """

    def __init__(self, name: str) -> None:
        super().__init__(name, level=DEBUG)

        # Define Log file name
        log_file = f'{name}.log'

        # Define console handler
        console_handler = StreamHandler(stdout)
        console_handler.setFormatter(FORMATTER)

        # Define file handler
        file_handler = TimedRotatingFileHandler(
            f'{LOG_DIR}/{log_file}', when='midnight')
        file_handler.setFormatter(FORMATTER)

        # Setup logger
        self.addHandler(console_handler)
        self.addHandler(file_handler)
        self.propagate = False
