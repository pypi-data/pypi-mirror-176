import os

from aws_lambda_powertools import Logger

logger = Logger()

REGION_NAME = os.getenv("AWS_REGION", 'eu-west-1')
