"""
    Logging module which implements MEH Nodejs standards.
"""
import logging
import traceback

from .utils import read_package
from .enums.levels import Levels
from .transports.stream import StreamTransport

# Defaults
DEFAULT_NAME = read_package.read_package_file().get("name", None)
DEFAULT_MIN_LEVEL = Levels.NOT_SET.value
DEFAULT_MAX_LEVEL = Levels.MAX_LEVEL.value


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Logger(Singleton):
    def __init__(self, name=DEFAULT_NAME):
        self.name = name

        logging.root.setLevel(DEFAULT_MIN_LEVEL)

        self.logger = logging.getLogger(name)
        self.add_transport(StreamTransport(level=Levels.DEBUG.value))

    def __str__(self):
        return f"<Logger name={self.name}>"

    def set_level(self, level):
        self.logger.setLevel(level)

        for handler in self.logger.handlers:
            handler.setLevel(level)

        return self

    # TODO: Remove this
    # def __overwrite_default_handler(self):
    #     handler = logging.StreamHandler()
    #     handler.setLevel(DEFAULT_MAX_LEVEL)

    #     return handler

    def __handle_stack(self, message):
        if isinstance(message, Exception):
            return {
                "stack": "".join(
                    traceback.TracebackException.from_exception(message).format()
                ),
            }

        return {"stack": None}

    def add_transport(self, handler):
        self.logger.addHandler(handler)
        return self

    def debug(self, message):
        return self.logger.log(
            Levels.DEBUG.value, message, extra=self.__handle_stack(message)
        )

    def info(self, message):
        return self.logger.log(
            Levels.INFO.value, message, extra=self.__handle_stack(message)
        )

    def warning(self, message):
        return self.logger.log(
            Levels.WARNING.value, message, extra=self.__handle_stack(message)
        )

    def error(self, message):
        return self.logger.log(
            Levels.ERROR.value, message, extra=self.__handle_stack(message)
        )

    def critical(self, message):
        return self.logger.log(
            Levels.CRITICAL.value, message, extra=self.__handle_stack(message)
        )


logger = Logger()
