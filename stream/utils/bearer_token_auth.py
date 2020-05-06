import requests
import logging

logger = logging.getLogger(__name__)

# Gets a bearer token
class BearerTokenAuth():
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_bearer_token(self):
        logger.info('Requesting new bearer token...')
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'TwitterDevCovid19StreamQuickStartPython'})
        if response.status_code is not 200:
            raise Exception(f'Cannot get a Bearer token (HTTP {response.status_code}): {response.text}')
        body = response.json()
        logger.info('... successfully obtained bearer token')
        return body['access_token']
