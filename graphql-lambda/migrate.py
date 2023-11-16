from botocore.exceptions import ClientError
import boto3

CARDS_TABLE = 'cards'
SECTIONS_TABLE = 'sections'
access_key_id = 'AKIAYBNJI4EPU7RHB3U3'
secret_access_key = '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'
region_name = "eu-north-1"


def createCardTable():
    # Code to add the item into dynamo db
    dynamodb = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    ).resource('dynamodb', region_name=region_name)
    try:
        table = dynamodb.create_table(
            TableName=CARDS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            table = dynamodb.Table(CARDS_TABLE)
        else:
            raise e


def createSectionTable():
    # Code to add the item into dynamo db
    dynamodb = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    ).resource('dynamodb', region_name=region_name)
    try:
        table = dynamodb.create_table(
            TableName=SECTIONS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            table = dynamodb.Table(SECTIONS_TABLE)
        else:
            raise e
