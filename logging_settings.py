"""Logging settings"""
import logging
import time


def set_logger():
    """Set logger properties"""

    level = logging.INFO
    message_format = "%(message)s"
    handlers = [
        logging.FileHandler(f"{logging_date()}_log.txt"),
        logging.StreamHandler(),
    ]
    logging.basicConfig(level=level, format=message_format, handlers=handlers)


def logging_date() -> str:
    """Format date for logging file
    Returns:
        str: date DD_MM_YYYY_HHMMSS
    """
    return time.strftime("%d_%m_%Y_%H%M%S")
