import logging.handlers

from module_07_logging_part_2.homework.hw1_add_logging.handlers import LevelFileHandler, ASCIIFilter

dict_config = {
    "version": 1,
    "disable_existing_logger": True,
    "formatters":{
        "base":{
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "handlers":{
        "http_handler": {
            "class": "logging.handlers.HTTPHandler",
            "level": "DEBUG",
            "host":"127.0.0.1:5000",
            "url":"/log",
            "method": "POST",
            "formatter": "base"
        },
        "console":{
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "filters": ["ascii_filter",],
            "formatter":"base"
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
            "filters": ["ascii_filter",],
            "interval": 10,
            "backupCount": 5
        }
    },
    "filters":{
      "ascii_filter":{
          "()": ASCIIFilter,
      }
    },
    "loggers":{
        "diff_logger":{
            "level": "DEBUG",
            "handlers": ["file_debug", "file_error", "console", "http_handler"]
            },
        "info_logger":{
            "level": "INFO",
            "handlers": ["file_info", "console"]
            }
        }
    }