import os
import logging
import requests
from json import loads, dumps

from dotenv import load_dotenv

load_dotenv()

JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_CLOUD_INSTANCE = os.getenv('JIRA_CLOUD_INSTANCE')

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
                logger.debug('Detected error on: {}'.format(sensor_data))

    return 0

def send_error_to_jira(payload):
    header = {"Authorization": JIRA_API_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"}

    request_url = f"{JIRA_CLOUD_INSTANCE}/rest/api/3/issue"

    issue_json = create_issue_json(payload)
    payload = json.dumps(issue_json)

    response = requests.post(request_url, headers=header, data=payload)

    return response

def create_issue_json(payload):

    error_message = f"Error found on {payload['device']['S']} executing the test {payload['test']['S']}"

    issue_json = {
        "fields": {
            "summary": error_message,
            "issuetype": {
                "name": "Task"
            },
            "project": {
                "key": "SD"
            },
        "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                    "type": "paragraph",
                    "content": [
                        {
                        "text": error_message,
                        "type": "text"
                        }
                    ]
                    }
                ]
            }
        }
    }

    return issue_json
