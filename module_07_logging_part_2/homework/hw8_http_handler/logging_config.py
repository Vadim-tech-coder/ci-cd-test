import logging.handlers

from handlers import LevelFileHandler, ASCIIFilter

dict_config = {
    "version": 1,
    "disable_existing_logger": False,
    "filters": {
        "ascii_filter": {
            "()": ASCIIFilter,
        }
    },
    "formatters":{
        "base":{
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "handlers":{
        "http_handler":{
            "class": "logging.handlers.HTTPHandler",
            "level": "DEBUG",
            "formatter":"base",
            "host": "127.0.0.1:5000",
            "url": "/log",
            "method": "POST"
        },
        "console":{
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter":"base",
            "filters": ["ascii_filter", ]
        },
        "file_debug":{
            "()": LevelFileHandler,
            "level": "DEBUG",
            "filename": "calc_debug.log",
            "mode": "a",
            "formatter":"base"
        },
        "file_error":{
            "()": LevelFileHandler,
            "level": "ERROR",
            "filename": "calc_error.log",
            "mode": "a",
            "formatter":"base"
        },

        "file_info":{
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": "utils.log",
            "formatter":"base",
            "when":"s",
            "interval": 10,
            "backupCount": 5,
            "filters": ["ascii_filter", ]
        }
    },
    "loggers":{
        "diff_logger":{
            "level": "DEBUG",
            "handlers": ["console", "file_info", "http_handler"]
            },
        "info_logger":{
            "level": "INFO",
            "handlers": ["console", "file_info"]
            }
        }
    }