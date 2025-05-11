# TODO переписать реализацию ini-файла в формате dict-конфигурации.
dict_logging = {
    "version": 1,
    "disable_existing_logger": False,
    "formatters":{
       "fileFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt":"%Y-%m-%dT%H:%M:%S%Z"
       },
        "consoleFormatter":{
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"
        }
    },
    "handlers":{
        "fileHandler":{
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "encoding": 'utf8',
            "formatter": "fileFormatter",
            "filename": "logfile.log"
        },
        "consoleHandler":{
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers":{
        "root": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"]
        },
        "appLogger": {
            "level":"DEBUG",
            "handlers":["consoleHandler","fileHandler"],
            "qualname":"appLogger",
            "propagate": False
        }
    }
}