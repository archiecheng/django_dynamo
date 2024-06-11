#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:15
# @Author  : Laiyong(Archie) Cheng
# @Site    : 
# @File    : create_dynamodb_table.py
# @Software: PyCharm
# your_app/management/commands/create_dynamodb_table.py

from django.core.management.base import BaseCommand
import boto3
from django.conf import settings

class Command(BaseCommand):
    help = 'Create DynamoDB table for sessions'

    def handle(self, *args, **options):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        table = dynamodb.create_table(
            TableName=settings.SESSION_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'session_key',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'session_key',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=settings.SESSION_TABLE_NAME)
        self.stdout.write(self.style.SUCCESS('Successfully created table'))
