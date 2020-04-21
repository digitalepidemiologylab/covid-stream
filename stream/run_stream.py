import os
import requests
import json
import time
import logging
from utils.stream_helpers import BearerTokenAuth
from utils.stream_rules import StreamRules
from utils.misc import report_error
import config
from urllib3.exceptions import ProtocolError
from http.client import IncompleteRead


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)-5.5s] [%(name)-12.12s]: %(message)s')
logger = logging.getLogger(__name__)

# Error counts
time_last_error = 0
error_count_last_hour = 0

# Obtain bearer token
auth = BearerTokenAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET)

stream_url = 'https://api.twitter.com/labs/1/tweets/stream/filter'

def stream_connect():
    # expand all these fields
    expansions = [
            'author_id',
            'referenced_tweets.id',
            'in_reply_to_user_id',
            'attachments.media_keys',
            'attachments.poll_ids',
            'geo.place_id']
    # make sure to use detailed format to get full tweet objects
    params = {
            'format': 'detailed',
            'expansions': ','.join(expansions)
            }
    logger.info('Connecting to stream...')
    response = requests.get(stream_url, auth=auth, stream=True, params=params)
    for line in response.iter_lines():
        if line:
            tweet = json.loads(line)
            logger.info(tweet)
            with open('output.jsonl', 'w') as f:
                f.write(json.dumps(tweet) + '\n')

def hold_your_horses(base_delay=60, error_threshold=10):
    """
    Waits a certain amount of time (based on number of errors in the last hour), but waits at least 1min.
    If number of errors in last hour exceed error_threshold, shuts down stream
    """
    global time_last_error
    global error_count_last_hour
    if error_count_last_hour > error_threshold:
        report_error(msg=f'Error threshold of {error_threshold} reached, shutting down.')
        sys.exit()
    if (time.time() - time_last_error) < 3600:
        # delay based on number of errors but not longer than 30min
        delay = min(base_delay * error_count_last_hour, 1800)
        error_count_last_hour += 1
    else:
        # reset counter
        error_count_last_hour = 1
        delay = base_delay
    time_last_error = time.time()
    logger.info(f'Sleeping for {delay:,} seconds')
    time.sleep(delay)

def rollbar_init():
    config = Config()
    if config.ENV == 'prd':
        rollbar.init(
                config.ROLLBAR_ACCESS_TOKEN,
                'production',
                root=os.path.dirname(os.path.realpath(__file__)), # server root directory, makes tracebacks prettier
                allow_logging_basic_config=False)

def main():
    stream_rules = StreamRules(auth)
    stream_rules.init()
    while True:
        try:
            stream_connect()
        except KeyboardInterrupt:
            logger.info('Shutting down...')
            sys.exit()
        except (ProtocolError, IncompleteRead) as e:
            # simply reconnect
            report_error(exception=True)
        except (ProtocolError, ConnectionError, ConnectionResetError) as e:
            # wait a little
            hold_your_horses()
        except Exception as e:
            report_error(msg='Uncaught stream exception', exception=True)
            hold_your_horses()

if __name__ == "__main__":
    main()
