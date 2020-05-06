import logging
import requests

logger = logging.getLogger(__name__)


class StreamRunner:
    def __init__(self, partition):
        self.partition = partition

    def get_url(self):
        return f'https://api.twitter.com/labs/1/tweets/stream/covid19?partition={self.partition}'

    def connect(self, bearer_token):
        url = self.get_url()
        headers = {
                'User-Agent': 'TwitterDevCovid19StreamQuickStartPython',
                'Authorization': f'Bearer {bearer_token}'
                }
        resp = requests.get(url, headers=headers, stream=True)
        return resp
