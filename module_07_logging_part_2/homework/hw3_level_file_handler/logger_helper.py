import logging


debug_handler = logging.FileHandler('calc_debug.log')
debug_handler.setLevel(logging.DEBUG)


error_handler = logging.FileHandler('calc_error.log')
error_handler.setLevel(logging.ERROR)

