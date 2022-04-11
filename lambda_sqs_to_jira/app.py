import os
import logging
import requests
from json import loads, dumps

from dotenv import load_dotenv

load_dotenv()

JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_CLOUD_INSTANCE = os.getenv('JIRA_CLOUD_INSTANCE')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

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
                send_error_to_jira(sensor_data)

    return 0


def send_error_to_jira(sensor_data):
    header = {"Authorization": JIRA_API_TOKEN,
              "Accept": "application/json",
              "Content-Type": "application/json"}

    request_url = f"{JIRA_CLOUD_INSTANCE}/rest/api/3/issue"

    issue_json = create_issue_json(sensor_data)
    sensor_data = json.dumps(issue_json)

    logger.debug("Sending issue to Jira project with key {JIRA_PROJECT_KEY}")
    response = requests.post(request_url, headers=header, data=sensor_data)
    logger.debug(f"The request status code is {response.status_code}")
    logger.debug(response.text)


def create_issue_json(sensor_data):
    logger.debug("Creating issue json from sensor data")
    error_message = f"Error found on {sensor_data['device']['S']} executing the test {sensor_data['test']['S']}"
    logger.debug(error_message)

    issue_json = {
        "fields": {
            "summary": error_message,
            "issuetype": {
                "name": "Task"
            },
            "project": {
                "key": JIRA_PROJECT_KEY,
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
