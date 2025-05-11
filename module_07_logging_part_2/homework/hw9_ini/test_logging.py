from dict_config import dict_logging
import logging.config

logging.config.dictConfig(dict_logging)

app_logger = logging.getLogger('appLogger')

app_logger.debug("debug message")
app_logger.info("info message")
app_logger.warning("warning message")
app_logger.error("error message")