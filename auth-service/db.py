# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from datetime import datetime
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
import util

dynamo_client = boto3.client('dynamodb')
user_table = 'User'


def get_user(username):
    return dynamo_client.query(
        TableName=user_table,
        KeyConditionExpression='Username = :username',
        ExpressionAttributeValues={
            ':username': {'S': str(username)}
        }
    )


def create_user(name, password):
    return dynamo_client.put_item(
        TableName=user_table,
        Item={
            'UserId': {'S': str(uuid.uuid4())},
            'Username': {'S': name},
            'Password': {'S': util.encrypt_string(password)},
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )


def check_password(username, password):
    response = dynamo_client.query(
        TableName=user_table,
        KeyConditionExpression='Username = :username',
        ExpressionAttributeValues={
            ':username': {'S': str(username)}
        },
        Limit=1
    )

    encrypted_password = str(util.encrypt_string(password))
    existing_password = ""
    
    if 'Items' in response:
        if response['Items']:
            existing_password = str(response['Items'][0]['Password']['S'])

    if existing_password.__eq__(encrypted_password):
        return {
            'Login': True,
            'Token': str(uuid.uuid4()) #TODO: update token generation with JWT
        }
    else:
        return {
            'Login': False,
        }

