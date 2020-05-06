# Covid stream
Code specific to the Twitter Labs endpoint for COVID-19 using Amazon Kinesis Firehose

Before you start, make sure to have `docker` as well as `docker-compose` installed on your host machine.

## Usage
1. Create an AWS delivery stream. Make sure to pick "PUT action" as source. Destination can be S3 in the simplest case.
2. Create an IAM user with `AmazonKinesisFirehoseFullAccess` permission
3. `git clone https://github.com/digitalepidemiologylab/covid-stream.git && cd covid-stream`
4. Copy the example secrets file `cp secrets.list.example secrets.list`
5. Open the file `secrets.list` and fill in `CONSUMER_KEY` and `CONSUMER_SECRET` of the app which links to the COVID stream. As well as the AWS credentials of the IAM user created under 2). You may want to provide a Rollbar token (for error notifications), feel free to leave empty.
6. Run either `source build_production.sh` (runs in the background) or `source build_development.sh`. This will launch 4 streams for each partition.

## Contact
Feel free to write to me if you have questions martin.muller@epfl.ch
