from enum import Enum


class AWSServices(Enum):
    SNS='sns'
    SQS='sqs'
    SECRETSMANAGER='secretsmanager'

class FilterOptions(Enum):
    ALL='all'
    ANY='any'