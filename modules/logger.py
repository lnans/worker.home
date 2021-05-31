import logging
import sys
from configparser import ConfigParser
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


class AppLogger:
    """
        Class to provide custom logging format
        Allow to log in different files.
        Files names are determined with the name passed to the get_logger function
    """

    __log_formatter: logging.Formatter
    __log_file: str
    __log_dir: str

    def __init__(self) -> None:
        config = ConfigParser()
        config.read('.config.ini')
        self.__log_dir = config.get('Settings', 'LogDir')
        self.__log_formatter = logging.Formatter(
            '%(asctime)s|%(name)s|%(levelname)s|%(message)s')
        Path(self.__log_dir).mkdir(exist_ok=True)

    def get_console_handler(self) -> logging.StreamHandler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.__log_formatter)
        return console_handler

    def get_file_handler(self) -> TimedRotatingFileHandler:
        file_handler = TimedRotatingFileHandler(
            f'{self.__log_dir}/{self.__log_file}', when='midnight')
        file_handler.setFormatter(self.__log_formatter)
        return file_handler

    def get_logger(self, logger_name) -> logging.Logger:
        self.__log_file = f'{logger_name}.log'
        logger = logging.getLogger(logger_name)
        # better to have too much log than not enough
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger
