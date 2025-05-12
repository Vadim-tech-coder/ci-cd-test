import logging
import sys
from logging_config import dict_config
from handlers import LevelFileHandler
from logging import config


def get_logger(name):
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(f"diff_logger.{name}")
    return logger

