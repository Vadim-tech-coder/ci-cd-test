import logging.config
from logging_config import dict_config

logging.config.dictConfig(dict_config)

# formatter_sub = logging.Formatter(fmt = "%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d")


root_logger = logging.getLogger()
# logging.basicConfig()
custom_handler_for_root = logging.StreamHandler()
custom_handler_for_root.setLevel('DEBUG')
root_logger.addHandler(custom_handler_for_root)
# custom_handler_for_root.formatter = formatter_sub


sub_1_logger = logging.getLogger('sub_1')
# sub_1_logger.setLevel('DEBUG')
# sub_1_logger.propagate = False


sub_2_logger = logging.getLogger('sub_2')
# sub_2_logger.setLevel('INFO')
#
sub_sub_1_logger = logging.getLogger('sub_2.sub_sub_1')
# sub_sub_1_logger.setLevel('DEBUG')
# sub_sub_1_logger.propagate = False

module_logger = logging.getLogger('module_logger')
module_logger.propagate = False

submodule_logger = logging.getLogger('module_logger.submodule_logger')
submodule_logger.setLevel('DEBUG')
submodule_logger.propagate = True

custom_handler = logging.StreamHandler()
module_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(message)s")
custom_handler.setFormatter(formatter)

file_handler = logging.FileHandler('applog.log', mode='a')
file_handler.setFormatter(formatter)
module_logger.addHandler(file_handler)

# custom_handler_for_sub = logging.StreamHandler()
# custom_handler_for_sub.setLevel('DEBUG')
# custom_handler_for_sub.formatter = formatter_sub
# sub_1_logger.addHandler(custom_handler_for_sub)
# sub_sub_1_logger.addHandler(custom_handler_for_sub)


def main():
    print("Root logger:")
    print(root_logger.handlers)

    print("Submodule logger:")
    print(submodule_logger.handlers)

    print("Module logger:")
    print(module_logger.handlers)

    submodule_logger.debug("Hi there!")

    print("sub_1 logger: ")
    print(sub_1_logger.handlers)

    print("sub_2 logger: ")
    print(sub_2_logger.handlers)

    print('sub_sub_1 logger: ')
    print(sub_sub_1_logger.handlers)

    sub_sub_1_logger.debug("IT IS DEBUG MODE!!! of sub_sub_1")
    sub_1_logger.debug("Debug from sub_1")
    sub_2_logger.debug("Debug from sub_2")


if __name__ == '__main__':
    main()
