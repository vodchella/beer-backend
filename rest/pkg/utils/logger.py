import logging.handlers
import os
import sys
from pkg.config import CONFIG
from pkg.constants.date_formats import DATE_FORMAT_FULL
from pkg.constants.logging import DEFAULT_LOGGER_NAME, DB_LOGGER_NAME, REST_LOGGER_NAME, LOGGING_FORMAT


LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': LOGGING_FORMAT,
            'datefmt': DATE_FORMAT_FULL
        }
    },
    'handlers': {
        'internal': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stderr
        },
        'timedRotatingFile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'when': 'midnight',
            'filename': os.path.join(CONFIG['log']['path'],
                                     CONFIG['log']['file_name'])
        }
    },
    'loggers': {
        DEFAULT_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile']
        },
        REST_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile']
        },
        DB_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile']
        },
    }
}


DEFAULT_LOGGER = logging.getLogger(DEFAULT_LOGGER_NAME)
REST_LOGGER = logging.getLogger(REST_LOGGER_NAME)
DB_LOGGER = logging.getLogger(DB_LOGGER_NAME)
