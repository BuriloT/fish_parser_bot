import logging
from logging.handlers import RotatingFileHandler

from constants import BASE_DIR

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_logging():
    log_dir = BASE_DIR / 'Logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'fish_parser.log'

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10**6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
