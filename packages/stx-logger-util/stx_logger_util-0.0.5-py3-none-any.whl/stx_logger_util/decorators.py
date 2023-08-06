# Python's Libraries
import logging
import inspect

# Own's Libraries
from .log_message import LogMessage
from .function_types import FunctionType


def get_FunctionType(_func):
    if inspect.getargspec(_func)[0][0] == 'self':
        return FunctionType.METHOD
    else:
        return FunctionType.SIMPLE_FUNCTION


def get_FunctionPath(_func, _args, _function_type):
    if _function_type == FunctionType.METHOD:
        return f'{_func.__module__}.{_args[0].__class__.__name__}.{_func.__name__}'
    else:
        return f"{_func.__module__}.{_func.__name__}"


def log(_level=1):
    def inner(func):
        def wrapper(*args, **kwargs):
            function_type = get_FunctionType(func)
            function_path = get_FunctionPath(func, args, function_type)
            logging.debug(LogMessage.get_Start(_level, args, function_path, function_type))
            try:
                response = func(*args, **kwargs)
                logging.debug(LogMessage.get_End(_level, "Success", function_path))
                return response

            except Exception as e:
                logging.error(LogMessage.get_End(_level, str(e), function_path))
                raise e

        return wrapper
    return inner
