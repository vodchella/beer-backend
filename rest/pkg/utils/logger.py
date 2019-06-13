import logging.handlers
import os
from pkg.config import CONFIG
from pkg.constants.date_formats import DATE_FORMAT_FULL
from pkg.constants.logging import DEFAULT_LOGGER, LOGGING_FORMAT
from pkg.utils.console import panic


def create_logger():
    result = logging.getLogger(DEFAULT_LOGGER)
    result.setLevel(logging.INFO)
    f = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=DATE_FORMAT_FULL)
    try:
        trfh = logging.handlers.TimedRotatingFileHandler(os.path.join(CONFIG['log']['path'],
                                                                      CONFIG['log']['file_name']),
                                                         'midnight')
    except:
        panic()

    trfh.setFormatter(f)
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    result.addHandler(trfh)
    result.addHandler(ch)

    return result


LOGGER = create_logger()
