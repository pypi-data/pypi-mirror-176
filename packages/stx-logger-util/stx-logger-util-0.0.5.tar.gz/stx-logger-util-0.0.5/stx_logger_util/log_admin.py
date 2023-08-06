# Python's Libraries
import logging
from enum import Enum


loggers = {}


class LogEnv(Enum):
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"

    @staticmethod
    def list():
        return list(map(lambda item: item.value, LogEnv))


class LogAdmin(object):

    @classmethod
    def __get_Level(self, _environment):
        if _environment == LogEnv.PRODUCTION:
            return logging.INFO

        return logging.DEBUG

    @classmethod
    def __get_MsgFormat(self, _timestamp):
        if _timestamp:
            return "%(asctime)s [%(levelname)s] %(message)s"

        return "[%(levelname)s] %(message)s"

    @classmethod
    def create_Logger(
        self,
        _environment=LogEnv.DEVELOPMENT,
        _name="app",
        _timestamp=False
    ):
        global loggers

        if loggers.get(_name):
            return loggers.get(_name)

        level = self.__get_Level(_environment)
        msg_format = self.__get_MsgFormat(_timestamp)

        logging.root.handlers = []
        logging.basicConfig(
            format=msg_format,
            datefmt='%m/%d/%Y %I:%M:%S %p' if _timestamp else None,
            level=level
        )

        logger = logging.getLogger(_name)
        loggers[_name] = logger

        return logger


# Only will show the messages of the set level or supperior

# LEVELS:
# - CRITICAL	50
# - ERROR	40
# - WARNING	30
# - INFO	20
# - DEBUG	10
# - NOTSET	0
