import sys
import traceback
from contextlib import contextmanager

import loguru
import ujson
from tchotchke.exceptions import LoggableError


class Logger:
    def __init__(self, log_sink=sys.stdout):
        self.__internal_logger = loguru.logger
        self.__internal_logger.remove()
        self.__internal_logger.add(log_sink, backtrace=True, diagnose=True, colorize=True)

    @contextmanager
    def log_uncaught_exceptions(self):
        try:
            yield
        except Exception as error:
            self.exception("an unhandled exception occurred", error)
            raise

    def debug(self, message, sprinkles=None):
        output_log = self.__format_output_log(message, sprinkles)
        serialized_output = ujson.dumps(output_log)
        self.__internal_logger.debug(serialized_output)

    def info(self, message, sprinkles=None):
        output_log = self.__format_output_log(message, sprinkles)
        serialized_output = ujson.dumps(output_log)
        self.__internal_logger.info(serialized_output)

    def warning(self, message, sprinkles=None):
        output_log = self.__format_output_log(message, sprinkles)
        serialized_output = ujson.dumps(output_log)
        self.__internal_logger.warning(serialized_output)

    def error(self, message, sprinkles=None):
        output_log = self.__format_output_log(message, sprinkles)
        serialized_output = ujson.dumps(output_log)
        self.__internal_logger.error(serialized_output)

    def exception(self, message, error, sprinkles=None):
        if sprinkles is None:
            sprinkles = {}
        if isinstance(error, LoggableError):
            sprinkles |= error.log_sprinkles
        output_log = self.__format_output_log(message, sprinkles)
        output_log["exception"] = traceback.format_exc()
        output_log["error_message"] = str(error)
        serialized_output = ujson.dumps(output_log)
        self.__internal_logger.error(serialized_output)

    @staticmethod
    def __format_output_log(message, raw_sprinkles):
        if not isinstance(message, str):
            raise TypeError()
        if not isinstance(raw_sprinkles, dict) and raw_sprinkles is not None:
            raise TypeError()
        sprinkles = Logger.route_recurse(raw_sprinkles)
        return {
            "message": message,
            "sprinkles": sprinkles
        }

    @staticmethod
    def route_recurse(value):
        if isinstance(value, list):
            return Logger.__repr_list(value)
        elif isinstance(value, dict):
            return Logger.__repr_dict(value)
        else:
            return repr(value)

    @staticmethod
    def __repr_list(sprinkles):
        result = []
        for value in sprinkles:
            formatted_value = Logger.route_recurse(value)
            result.append(formatted_value)
        return result

    @staticmethod
    def __repr_dict(sprinkles):
        result = {}
        for key, value in sprinkles.items():
            formatted_value = Logger.route_recurse(value)
            result[key] = formatted_value
        return result
