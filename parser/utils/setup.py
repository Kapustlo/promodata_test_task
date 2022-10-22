import logging
import logging.config
from pathlib import Path

from parser.settings import Settings


def init_logging(settings: Settings):
    handlers = {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    }

    if settings.logs_dir:
        path = Path(settings.logs_dir)

        handlers['file'] = {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(path / 'parser.txt'),
            'formatter': 'verbose',
            'maxBytes': 8 * 1024 * 1024 * 5,
            'backupCount': 10
        }

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': handlers,
        'loggers': {
            'parser': {
                'handlers': handlers.keys(),
                'level': 'DEBUG',
                'propagate': True
            }
        },
        'formatters': {
            'verbose': {
                'format': '-' * 8 + '\n[{levelname} | {asctime} | ({module})]:\n{message}\n' + '-' * 8 + '\n',
                'style': '{',
            },
        },
    }

    logging.config.dictConfig(config)


def init(settings: Settings):
    init_logging(settings)
