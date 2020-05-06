import os
import sys
import json
import time
import boto3
import logging
import rollbar
import config
from utils.bearer_token_auth import BearerTokenAuth
from utils.stream_runner import StreamRunner
from utils.misc import report_error, TwitterError
from urllib3.exceptions import ProtocolError
from http.client import IncompleteRead
from threading import Thread


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)-5.5s] [%(name)-12.12s]: %(message)s')
logger = logging.getLogger(__name__)

# Error counts
time_last_error = 0
error_count_last_hour = 0

# Firehose client
client = boto3.client('firehose',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

def stream_connect(partition):
    logger.info(f'Connecting to stream partition {partition}...')
    stream = StreamRunner(partition)
    auth = BearerTokenAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    bearer_token = auth.get_bearer_token()
    resp = stream.connect(bearer_token)
    if resp.status_code != 200:
        try:
            te = TwitterError(data=resp.json(), status_code=resp.status_code)
        except:
            raise Exception(resp)
        raise te
    logger.info(f'Successfully connected to stream. Starting to collect data...')
    count = 0
    for line in resp.iter_lines():
        if line:
            # add to AWS delivery stream
            client.put_record(DeliveryStreamName=config.AWS_DELIVERY_STREAM_NAME, Record={'Data': line + '\n'.encode()})
            # some logging
            count += 1
            if count % 100 == 0:
                logger.info(f'Collected {count:,} tweets...')

def hold_your_horses(base_delay=1000, error_threshold=10, max_delay=3600):
    """
    Waits a certain amount of time (based on number of errors in the last hour), but waits at least 1000sec (>15min).
    If number of errors in last hour exceed error_threshold, shuts down stream
    """
    global time_last_error
    global error_count_last_hour
    if error_count_last_hour > error_threshold:
        report_error(msg=f'Error threshold of {error_threshold} reached, shutting down.')
        sys.exit()
    if (time.time() - time_last_error) < 3600:
        # delay based on number of errors but not longer than max_delay
        delay = min(base_delay * error_count_last_hour, max_delay)
        error_count_last_hour += 1
    else:
        # reset counter
        error_count_last_hour = 1
        delay = base_delay
    time_last_error = time.time()
    logger.info(f'Sleeping for {delay:,} seconds')
    time.sleep(delay)

def rollbar_init():
    if config.ROLLBAR_ACCESS_TOKEN == '':
        logger.info('Rollbar access token has not been set. Ignoring.')
        return
    rollbar.init(
            config.ROLLBAR_ACCESS_TOKEN,
            'production',
            root=os.path.dirname(os.path.realpath(__file__)), # server root directory, makes tracebacks prettier
            allow_logging_basic_config=False,
            enabled=config.ENV == 'prd') # only activate in production

def main():
    # Initialize rollbar
    rollbar_init()
    partition = sys.argv[1]
    while True:
        try:
            stream_connect(partition)
        except KeyboardInterrupt:
            logger.info('Shutting down...')
            sys.exit()
        except (ProtocolError, IncompleteRead) as e:
            logger.warning(e)
            # simply reconnect
            report_error(exception=True)
        except (ProtocolError, ConnectionError, ConnectionResetError) as e:
            logger.warning(e)
            report_error(exception=True)
            # wait a little
            hold_your_horses()
        except TwitterError as e:
            report_error(msg=str(e), exception=True)
            hold_your_horses()
        except Exception as e:
            logger.error('Uncaught stream exception')
            if config.ENV == 'dev':
                raise e
            report_error(msg='Uncaught stream exception', exception=True)
            hold_your_horses()

if __name__ == "__main__":
    main()
