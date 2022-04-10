import logging
from json import loads


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.debug('Received event: '.format(event))

    for record in event['Records']:
        payload = loads(record['body'], parse_float=str)
        sensor_data = payload['Item']

        logger.debug('Payload received: {}'.format(payload))

        if 'status' in sensor_data.keys():
            if sensor_data['status']['S'] == 'ERROR':
                logger.debug('Detected error on: {}'.format(payload))

    return 0
