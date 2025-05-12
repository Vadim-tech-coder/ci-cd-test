import logging


class LevelFileHandler(logging.FileHandler):

    def __init__(self, filename, mode='a'):
        super().__init__(filename, mode)

class LevelFilter(logging.Filter):


    def __init__(self, level):
        super().__init__()
        self.level = level


    def filter(self, record):
        return record.levelno == self.level
