import logging
import requests

logger = logging.getLogger(__name__)


class StreamRunner:
    def __init__(self):
        # expand all these fields
        expansions = [
                'author_id',
                'referenced_tweets.id',
                'in_reply_to_user_id',
                'attachments.media_keys',
                'attachments.poll_ids',
                'geo.place_id']
        # make sure to use detailed format to get full tweet objects
        self.params = {
                'format': 'detailed',
                'expansions': ','.join(expansions)
                }
        self.connection = None

    def get_url(self, partition):
        return f'https://api.twitter.com/labs/1/tweets/stream/covid19?partition={partition}'

    def connect(self, bearer_token, partition):
        url = self.get_url(partition)
        headers = {
                'User-Agent': 'TwitterDevCovid19StreamQuickStartPython',
                'Authorization': f'Bearer {bearer_token}'
                }
        resp = requests.get(url, headers=headers, stream=True)
        logger.info(resp)
        return resp
