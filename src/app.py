import os
import logging
import json

from pathlib import Path
from datetime import datetime
# import requests

logger: logging.Logger = None

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    setup_logging()

    logger.info("info message from logger")

    logger.info(f"Event is {event}")

    logger.debug("debug message from logger")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

def setup_logging(local_run=False, log_level=None):
    global logger
    if logger is None:
        # Setup logging
        log_level = log_level if log_level else os.getenv('LOG_LEVEL')
        log_level = log_level.upper() if log_level else logging.INFO
        
        if local_run:
            logger = logging.getLogger(__file__)
            handlers = [logging.StreamHandler()]
            log_directory = Path(__file__).parent.parent.resolve() / 'logs'
            if not log_directory.exists():
                log_directory.mkdir()
            handlers.append(logging.FileHandler(filename=f'{log_directory}/{datetime.now().timestamp()}.log'))

            logging.basicConfig(
                level=log_level,
                format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                handlers=handlers
            )
        else:
            logger = logging.getLogger()
            logger.setLevel(log_level)

if __name__ == '__main__':

    setup_logging(local_run=True, log_level='info')
    lambda_handler(None, None)
