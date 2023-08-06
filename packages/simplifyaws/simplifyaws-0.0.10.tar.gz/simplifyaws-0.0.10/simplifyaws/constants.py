from enum import Enum


class Services(Enum):
    SNS='sns'
    SQS='sqs'
    SECRETSMANAGER='secretsmanager'

class FilterOptions(Enum):
    ALL='all'
    ANY='any'