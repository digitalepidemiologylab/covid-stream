import requests
import logging
import json

logger = logging.getLogger(__name__)

class StreamRules:
    """ Add/remove rules for filter streams. """
    def __init__(self, auth):
        self.rules_url = "https://api.twitter.com/labs/1/tweets/stream/filter/rules"
        self.config_path = 'rules.json'
        self.auth = auth

    def init(self):
        current_rules = self.list_rules()
        config = self.read_config()
        if current_rules != config:
            logger.info('Updating rules...')
            self.delete_rules(current_rules)
            self.set_rules(config)
        else:
            logger.info('Current rules are up to date!')

    def read_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config

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
