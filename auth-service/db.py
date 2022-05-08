# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from datetime import datetime
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid

dynamo_client = boto3.client('dynamodb')
wallet_table = 'Wallet'
transaction_table = 'Transaction'


def get_wallet(user_id):
    return dynamo_client.query(
        TableName=wallet_table,
        KeyConditionExpression='UserId = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': str(user_id)}
        }
    )


def create_wallet(user_id, address):
    return dynamo_client.put_item(
        TableName=wallet_table,
        Item={
            'UserId': {'S': user_id},
            'Address': {'S': address},
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )


def add_funds(address, currency, amount):
    total = get_wallet_total(address)

    if total == 0:
        total = {
            "L": [
                {
                    "M": {
                        "Currency": {
                            "S": currency
                        },
                        "Amount": {
                            "N": amount
                        }
                    }
                }
            ]
        }
    # TODO: add logic to update total attribute

    return dynamo_client.put_item(
        TableName=transaction_table,
        Item={
            'Id': {'S': str(uuid.uuid4())},
            'Address': {'S': address},
            'Currency': {'S': currency},
            'Amount': {'N': amount},
            'Type': {'S': 'CR'},
            'Total': total,
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )


def get_wallet_total(address):
    response = dynamo_client.query(
        TableName=transaction_table,
        KeyConditionExpression='Address = :address',
        ExpressionAttributeValues={
            ':address': {'S': address}
        },
        ScanIndexForward=False,
        Limit=1,
    )

    if 'Items' in response:
        if response['Items']:
            return response['Items'][0]['Total']

    return 0
