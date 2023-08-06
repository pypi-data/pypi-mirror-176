# Own's Libraries
from .function_types import FunctionType


class LogMessage(object):

    @classmethod
    def __clean_ParamValue(self, _param):
        value = _param

        if _param is None:
            value = "None"

        return value

    @classmethod
    def __build_ParamString(self, _params_str, _qty_flag, _qty_args, _value):
        if _qty_flag == _qty_args:
            _params_str += f"{_value}"
        else:
            _params_str += f"{_value}, "

        return _params_str

    @classmethod
    def __build_Prefix(self, _level):
        prefix = ""
        for n in range(int(_level)):
            if n == 0:
                continue

            prefix += "..."

        if isinstance(_level, float):
            level_str = str(_level)
            level_part = level_str.split('.')[1]

            if int(level_part) > 2:
                raise ValueError("Decimal part is greates than 2")

            for n in range(int(level_part)):
                prefix += "."

        return prefix

    @classmethod
    def __get_Message(self, _pre_message, _level):
        prefix = self.__build_Prefix(_level)

        if prefix:
            message = f"{prefix} {_pre_message}"
        else:
            message = _pre_message

        return message

    @classmethod
    def get_Start(self, _level, _args, _func_path, _func_type):
        qty_flag = 0
        qty_args = len(_args)
        params_str = ""

        for param in _args:
            qty_flag += 1

            if _func_type == FunctionType.METHOD \
                    and qty_flag == 1:
                continue

            value = self.__clean_ParamValue(param)
            params_str = self.__build_ParamString(params_str, qty_flag, qty_args, value)

        pre_message = f"{_func_path}({params_str})"
        message = self.__get_Message(pre_message, _level)

        return message

    @classmethod
    def get_End(self, _level, _result, _func_path):
        pre_message = f"{_func_path}: {_result}"
        return self.__get_Message(pre_message, _level)
