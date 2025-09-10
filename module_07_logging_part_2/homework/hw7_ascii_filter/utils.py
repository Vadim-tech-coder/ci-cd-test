import sys
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from logger_helper import get_logger, get_logger_info
from logging import config
from logging_config import dict_config


utils_logger = logging.getLogger('info_logger.utils')


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
    utils_logger.info("utils_logger INFO")
    utils_logger.warning("utils_logger WARNING")
    utils_logger.debug("utils_logger DEBUG")
    utils_logger.error("utils_logger ERROR")
    utils_logger.critical("utils_logger CRITICAL")
    utils_logger.info("йцукен")
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type: {value}")
        # print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        print(utils_logger)
        utils_logger.error(f"wrong operator value: {value}",  exc_info=False)
        # print("wrong operator value", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
