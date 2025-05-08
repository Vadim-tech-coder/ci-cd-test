import logging
import sys


class LevelFileHandler(logging.Handler):

    def __init__(self, filename, mode='a'):
        super().__init__()
        self.filename = filename
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        if record.levelname == 'DEBUG':
            self.filename = 'calc_debug.log'
        elif record.levelname == 'ERROR':
            self.filename = 'calc_error.log'
        with open(self.filename, mode = self.mode) as file:
            file.write(message + '\n')


def get_logger(name):
    logging.basicConfig(
        format = '%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s',
        level = 'DEBUG',
        handlers=[LevelFileHandler('logger.log'), logging.StreamHandler()]
    )
    logger = logging.getLogger(f"diff_level.{name}")
    return logger

