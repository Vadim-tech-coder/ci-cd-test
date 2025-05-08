import sys
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import get_logger


# logging.basicConfig()
# utils_logger = logging.getLogger('utils_logger')
# utils_logger.setLevel('DEBUG')
# utils_logger.propagate = False

utils_logger = get_logger('utils')

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s'))
# utils_logger.addHandler(handler)



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
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type: {value}")
        # print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        utils_logger.error(f"wrong operator value: {value}",  exc_info=False)
        # print("wrong operator value", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
