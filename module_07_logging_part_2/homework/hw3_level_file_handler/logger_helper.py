import logging
import sys
from module_07_logging_part_2.homework.hw4_dict_config.logging_config import dict_config
from module_07_logging_part_2.homework.hw1_add_logging.handlers import LevelFileHandler
from logging import config


def get_logger(name):
    # logging.basicConfig(
    #     format = '%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s',
    #     level = 'DEBUG',
    #     handlers=[LevelFileHandler('logger.log'), logging.StreamHandler()]
    # )
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(f"diff_logger.{name}")
    return logger

