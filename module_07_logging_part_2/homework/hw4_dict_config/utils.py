import sys
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import get_logger


utils_logger = get_logger('utils')


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    # print(utils_logger.handlers)
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type: {value}")
        # print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        utils_logger.error(f"wrong operator value: {value}",  exc_info=False)
        # print("wrong operator value", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
