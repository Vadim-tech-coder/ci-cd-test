from handlers import LevelFileHandler

dict_config = {
    "version": 1,
    "disable_existing_logger": True,
    "formatters":{
        "base":{
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class": "logging.StreamHandler",
            "level": "DEBUG",
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
        }
    },
    "loggers":{
        "diff_logger":{
            "level": "DEBUG",
            "handlers": ["file_debug", "file_error", "console"]
            }
        }
    }