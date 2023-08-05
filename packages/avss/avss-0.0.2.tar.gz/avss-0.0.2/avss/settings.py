import configparser
import logging
from pathlib import Path

global _LOGGER
_LOGGER = None
global _SETTINGS
_SETTINGS = None

BASE_PATH = Path(__file__).parent


def get_settings():
    global _SETTINGS
    if _SETTINGS is None:
        _SETTINGS = configparser.ConfigParser()
        with open(BASE_PATH.joinpath('config.ini')) as f:
            _SETTINGS.read_file(f)
    return _SETTINGS


def get_logger():
    global _LOGGER
    if _LOGGER is None:
        logging.basicConfig()
        logging.root.setLevel(logging.DEBUG)
        _LOGGER = logging.getLogger()

    return _LOGGER
