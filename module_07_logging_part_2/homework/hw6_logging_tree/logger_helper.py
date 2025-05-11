import logging
import sys
from logging_config import dict_config
from handlers import LevelFileHandler
from logging import config


def get_logger(name):
    logger = logging.getLogger(f"diff_logger.{name}")
    return logger



def get_logger_info(name):
    logger = logging.getLogger(f"info_logger.{name}")
    return logger