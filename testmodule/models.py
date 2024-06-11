from django.db import models

# Create your models here.
# testmodule/models.py

import boto3
from django.conf import settings

dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

class Item:
    def __init__(self):
        self.table = dynamodb.Table('items_table')

    def create_item(self, item_id, name, description):
        response = self.table.put_item(
            Item={
                'item_id': item_id,
                'name': name,
                'description': description,
            }
        )
        return response

    def get_item(self, item_id):
        response = self.table.get_item(Key={'item_id': item_id})
        return response.get('Item', None)

    def update_item(self, item_id, name=None, description=None):
        update_expression = []
        expression_attribute_names = {}
        expression_attribute_values = {}

        if name:
            update_expression.append('#n = :name')
            expression_attribute_names['#n'] = 'name'
            expression_attribute_values[':name'] = name

        if description:
            update_expression.append('description = :description')
            expression_attribute_values[':description'] = description

        update_expression_str = "SET " + ", ".join(update_expression)

        response = self.table.update_item(
            Key={'item_id': item_id},
            UpdateExpression=update_expression_str,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )
        return response

    def delete_item(self, item_id):
        response = self.table.delete_item(Key={'item_id': item_id})
        return response
