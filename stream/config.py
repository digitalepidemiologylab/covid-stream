import os

ENV=os.environ.get('ENV', 'dev')

# Twitter
CONSUMER_KEY = os.environ.get('CONSUMER_KEY', '')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', '')

# AWS
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION=os.environ.get('AWS_REGION', '')
AWS_DELIVERY_STREAM_NAME=os.environ.get('AWS_DELIVERY_STREAM_NAME', '')

# Rollbar
ROLLBAR_ACCESS_TOKEN = os.environ.get('ROLLBAR_ACCESS_TOKEN', '')
