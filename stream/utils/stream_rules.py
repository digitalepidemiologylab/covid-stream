import requests
import logging

logger = logging.getLogger(__name__)

sample_rules = [
    { 'value': 'dog has:images', 'tag': 'dog pictures' },
    { 'value': 'cat has:images -grumpy', 'tag': 'cat pictures' },
]

class StreamRules:
    def __init__(self, auth):
        self.rules_url = "https://api.twitter.com/labs/1/tweets/stream/filter/rules"
        self.auth = auth

    def init(self):
        logger.info('Initializing rules')
        current_rules = self.list_rules()
        print(current_rules)
        # self.delete_rules(current_rules)
        # self.set_rules(sample_rules)

    def list_rules(self):
        response = requests.get(self.rules_url, auth=self.auth)
        if response.status_code is not 200:
            raise Exception(f'Cannot get rules (HTTP {response.status_code}: {response.text})')
        return response.json()

    def delete_rules(self, rules):
        ids = list(map(lambda rule: rule['id'], rules['data']))
        payload = {
            'delete': {
                'ids': ids
            }
        }
        response = requests.post(self.rules_url, auth=self.auth, json=payload)
        if response.status_code is not 200:
            raise Exception(f'Cannot delete rules (HTTP {response.status_code}: {response.text})')
        logger.info(f'Successfully deleted rules {rules}')

    def set_rules(self, rules):
        if rules is None:
            return
        payload = {'add': rules}
        response = requests.post(self.rules_url, auth=self.auth, json=payload)
        if response.status_code is not 201:
            raise Exception(f'Cannot create rules (HTTP {response.status_code}: {response.text})')
        logger.info(f'Successfully set rules {rules}')
