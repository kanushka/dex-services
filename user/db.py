# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from datetime import datetime
import boto3
import uuid
import util

dynamo_client = boto3.client('dynamodb')
user_table = 'User'


def get_user(email):
    return dynamo_client.query(
        TableName=user_table,
        KeyConditionExpression='Email = :email',
        ExpressionAttributeValues={
            ':email': {'S': str(email)}
        },
        ProjectionExpression='UserId,Email,CreatedAt'
    )


def get_full_user(email):
    return dynamo_client.query(
        TableName=user_table,
        KeyConditionExpression='Email = :email',
        ExpressionAttributeValues={
            ':email': {'S': str(email)}
        }
    )


def create_user(email, password, name):
    return dynamo_client.put_item(
        TableName=user_table,
        Item={
            'UserId': {'S': str(uuid.uuid4())},
            'Email': {'S': email},
            'Password': {'S': password},
            'Name': {'S': name},
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )


def check_password(email, password):
    response = dynamo_client.query(
        TableName=user_table,
        KeyConditionExpression='Email = :email',
        ExpressionAttributeValues={
            ':email': {'S': str(email)}
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
            # TODO: update token generation with JWT
            'Token': str(uuid.uuid4())
        }
    else:
        return {
            'Login': False,
        }
