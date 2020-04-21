import logging
import requests

logger = logging.getLogger(__name__)


class StreamRunner:
    def __init__(self):
        self.stream_url = 'https://api.twitter.com/labs/1/tweets/stream/filter'
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

    def connect(self, auth):
        self.connection = requests.get(self.stream_url, auth=auth, stream=True, params=self.params)
        return self.connection
