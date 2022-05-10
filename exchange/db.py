# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from datetime import datetime
import boto3
import uuid

dynamo_client = boto3.client('dynamodb')
transaction_table = 'Transaction'

def exchange(address, from_currency, from_amount, to_currency, to_amount):
    total = get_wallet_total(address)

    if total == 0:
        total = {
            "L": [
                {
                    "M": {
                        "Currency": {
                            "S": from_currency
                        },
                        "Amount": {
                            "N": from_amount
                        }
                    }
                }
            ]
        }
    # TODO: add logic to update total attribute

    debit_response = dynamo_client.put_item(
        TableName=transaction_table,
        Item={
            'Id': {'S': str(uuid.uuid4())},
            'Address': {'S': address},
            'Currency': {'S': from_currency},
            'Amount': {'N': from_amount},
            'Type': {'S': 'DR'},
            'Total': total,
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )

    credit_response = dynamo_client.put_item(
        TableName=transaction_table,
        Item={
            'Id': {'S': str(uuid.uuid4())},
            'Address': {'S': address},
            'Currency': {'S': to_currency},
            'Amount': {'N': to_amount},
            'Type': {'S': 'CR'},
            'Total': total,
            'CreatedAt': {'S': datetime.utcnow().isoformat()}
        }
    )
    #TODO: update this logic with batch_writer() method
    return credit_response


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
