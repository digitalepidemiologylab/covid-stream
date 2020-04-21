import rollbar
import sys
import logging

logger = logging.getLogger(__name__)


def report_error(msg='', level='error', exception=False):
    # exception reporting
    if exception:
        rollbar.report_exc_info(sys.exc_info())
    # logging
    if level == 'warning' and msg != '':
        logger.warning(msg)
    if msg != '':
        logger.error(msg)
        rollbar.report_message(msg, level)
