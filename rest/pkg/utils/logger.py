import logging.handlers
import os
import sys
from logdna import LogDNAHandler
from pkg.config import CONFIG
from pkg.constants.date_formats import DATE_FORMAT_FULL
from pkg.constants.logging import *


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
        },
        'logdna': {
            'class': 'logging.handlers.LogDNAHandler',
            'key': CONFIG['log']['logdna_key'],
            'options': {
                'app': 'My Beer',
            },
        }
    },
    'loggers': {
        DEFAULT_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile', 'logdna']
        },
        REST_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile', 'logdna']
        },
        DB_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['internal', 'timedRotatingFile', 'logdna']
        },
        LOGDNA_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['logdna']
        }
    }
}


DEFAULT_LOGGER = logging.getLogger(DEFAULT_LOGGER_NAME)
REST_LOGGER = logging.getLogger(REST_LOGGER_NAME)
DB_LOGGER = logging.getLogger(DB_LOGGER_NAME)
LOGDNA_LOGGER = logging.getLogger(LOGDNA_LOGGER_NAME)
