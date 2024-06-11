#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:12
# @Author  : Laiyong(Archie) Cheng
# @Site    : 
# @File    : dynamodb_session_backend.py
# @Software: PyCharm

# your_app/dynamodb_session_backend.py

import boto3
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.utils import timezone
from datetime import timedelta

dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

class DynamoDBSession(SessionBase):
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.table = dynamodb.Table(settings.SESSION_TABLE_NAME)

    def load(self):
        try:
            response = self.table.get_item(Key={'session_key': self.session_key})
            if 'Item' in response:
                item = response['Item']
                expire_date = item['expire_date']
                if expire_date < timezone.now().timestamp():
                    self.create()
                    return {}
                return self.decode(item['session_data'])
            else:
                self.create()
                return {}
        except Exception:
            self.create()
            return {}

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        expire_date = (timezone.now() + timedelta(seconds=settings.SESSION_COOKIE_AGE)).timestamp()
        item = {
            'session_key': self.session_key,
            'session_data': self.encode(self._get_session(no_load=must_create)),
            'expire_date': expire_date,
        }
        if must_create:
            condition = 'attribute_not_exists(session_key)'
        else:
            condition = None
        self.table.put_item(Item=item, ConditionExpression=condition)
        self.modified = False

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        self.table.delete_item(Key={'session_key': session_key})

    @classmethod
    def clear_expired(cls):
        scan_kwargs = {
            'FilterExpression': 'expire_date < :now',
            'ExpressionAttributeValues': {
                ':now': timezone.now().timestamp()
            }
        }
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = cls.table.scan(**scan_kwargs)
            for item in response.get('Items', []):
                cls.table.delete_item(Key={'session_key': item['session_key']})
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

# 添加 SessionStore 类
class SessionStore(DynamoDBSession):
    pass