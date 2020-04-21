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


class TwitterError(Exception):
    def __init__(self, data={}, status_code=400):
        self.title = data.get('title')
        self.detail = data.get('detail')
        self.type = data.get('type')
        self.status_code = status_code

    def __str__(self):
        return f'[Error code {self.status_code}] {self.title}: {self.detail}'
