#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:33
# @Author  : Laiyong(Archie) Cheng
# @Site    : 
# @File    : create_items_table.py
# @Software: PyCharm
# testmodule/management/commands/create_items_table.py

from django.core.management.base import BaseCommand
import boto3
from django.conf import settings

class Command(BaseCommand):
    help = 'Create DynamoDB table for items'

    def handle(self, *args, **options):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        table = dynamodb.create_table(
            TableName='items_table',
            KeySchema=[
                {
                    'AttributeName': 'item_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'item_id',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='items_table')
        self.stdout.write(self.style.SUCCESS('Successfully created table'))
