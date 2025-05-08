import sys

from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import get_logger
from utils import string_to_operator
import logging



# logging.basicConfig()
# main_logger = logging.getLogger('main_logger')
# main_logger.setLevel('DEBUG')
# main_logger.propagate = False

main_logger = get_logger('main')

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s'))
# main_logger.addHandler(handler)


def calc(args):
    # print(main_logger.handlers)
    main_logger.info(f"Arguments: {args}")
    # print("Arguments: ", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        main_logger.error("Error while converting number 1", exc_info = e)
        # print("Error while converting number 1")
        # print(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        main_logger.error("Error while converting number 2", exc_info = e)
        # print("Error while converting number 2")
        # print(e)

    try:
        operator_func = string_to_operator(operator)
        result = operator_func(num_1, num_2)
        main_logger.info(f"Result: {result}")
        # print("Result: ", result)
        print(f"{num_1} {operator} {num_2} = {result}")
    except Exception as e:
        main_logger.error("Critical error", exc_info=True)






if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2%3')
