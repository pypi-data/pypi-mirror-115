# -*- coding: utf-8 -*-
import google.cloud.logging
import logging


def remove_root_logger_stdout():
    """Remove StreamHandler from root logger.

    An alternative way to do this is to edit zope.ini (wsgi config)
    and remove the handler there.
    """
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            logger.info(f"Removing StreamHandler from root logger - turning OFF logging to stdout")
            logger.removeHandler(handler)


# After this code runs, logger will not stream to stdout
remove_root_logger_stdout()

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.get_default_handler()
client.setup_logging()
