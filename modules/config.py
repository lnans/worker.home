
import configparser


PARSER = configparser.ConfigParser()
PARSER.read('.config.ini')

class Config:
    """
        Config Wrapper to get values in the .config.ini file
    """

    """ Get a string value from .config.ini file """
    @staticmethod
    def get(section: str, param: str) -> str:
        return PARSER.get(section, param)

    """ Get a int value from .config.ini file """
    @staticmethod
    def get_int(section: str, param: str) -> str:
        return PARSER.getint(section, param)
