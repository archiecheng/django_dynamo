#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:32
# @Author  : Laiyong(Archie) Cheng
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# testmodule/urls.py

from django.urls import path
from . import views

app_name = 'testmodule'

urlpatterns = [
    path('item/form', views.item_form, name='item_form'),
    path('item/create/', views.create_item, name='create_item'),
    path('item/<str:item_id>/', views.get_item, name='get_item'),
    path('item/update/<str:item_id>/', views.update_item, name='update_item'),
    path('item/delete/<str:item_id>/', views.delete_item, name='delete_item'),
]
