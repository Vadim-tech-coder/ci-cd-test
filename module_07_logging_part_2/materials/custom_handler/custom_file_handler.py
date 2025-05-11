import logging
import sys

class CustomFileHandler(logging.Handler):

    def __init__(self, file_name, mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(self.file_name, mode=self.mode) as f:
            f.write(message + str(vars(record)) + '\n')


class CustomStreamHandler(logging.StreamHandler):

    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stderr
        super().__init__(stream)


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "custom_handler": {
            "()": CustomStreamHandler,
            "level": "DEBUG",
            "formatter": "base"
        },
        "file": {
            "()": CustomFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "file_name": "customlogfile.log",
            "mode": "a"
        }
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["file", "custom_handler"],
            # "propagate": False,
        }
    },

    # "filters": {},
    # "root": {} # == "": {}
}
