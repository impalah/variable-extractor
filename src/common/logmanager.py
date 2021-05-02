"""
    Log manager
    * It is very simple and could have been done in the main class but it is here for future extensibility
    * This logger uses console logging and a simple text format.

"""

import json
import sys
import getopt
import os
import logging
import logging.config


class LogManager(object):

    logger = None

    def __init__(self):
        """
            Initializes logging
        """

        self.init_logging()

    def critical(self, msg, *args, **kwargs):
        """
            Utility method for logging with a CRITICAL logging level
        """
        self.logger.critical(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
            Utility method for logging with a ERROR logging level
        """
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
            Utility method for logging with a EXCEPTION logging level
        """
        self.logger.exception(msg, *args, exc_info=True, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
            Utility method for logging with a WARNING logging level
        """
        self.logger.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
            Utility method for logging with a INFO logging level
        """
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
            Utility method for logging with a DEBUG logging level
        """
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
            Logging with the specified log level
        """
        self.logger.log(level, msg, *args, **kwargs)


    def init_logging(self):
        """
            Initilialize logging
        """

        self.logger = logging.getLogger(__name__)

        # Get logging level from environment (docker/kubernetes)
        logging_level = int(os.getenv('EX1_LOGGING_LEVEL', logging.DEBUG))
        self.logger.setLevel(logging_level)

        # create console handler and set level to debug
        # Handler could be recovered from configuration file or environment variables
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)

        # create formatter: format could be recovered from an hypotetical ConfigManager or from environment variables
        formatter = logging.Formatter(
            '<%(asctime)s> - [%(levelname)s] - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
