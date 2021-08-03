import logging
from datetime import datetime

from . import ROOT_PATH
from .exception import SingletonException


class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("MainLogger")

    def set_config(self):
        file_handler = logging.FileHandler(
            "/home/ismail/Projects/GabTag"
            + "/logs/{:%Y-%m-%d}.log".format(datetime.now())
        )
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.set_config()
        self.logger.debug(message)

    def info(self, message):
        self.set_config()
        self.logger.info(message)

    def warning(self, message):
        self.set_config()
        self.logger.warning(message)

    def error(self, message):
        self.set_config()
        self.logger.error(message)

    def critical(self, message):
        self.set_config()
        self.logger.critical(message)


LOGGER = Logger()
