#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse
from stark.service.v1 import site, StarkHandler
from app01 import models


class DepartHandler(StarkHandler):
    display_list = ['id', 'title']

site.register(models.Depart, DepartHandler)


class UserInfoHandler(StarkHandler):
    # 定制页面显示的列
    display_list = ['name', 'age', 'email', 'depart']

    def get_display_list(self):

        return ['name', 'age']

site.register(models.UserInfo, UserInfoHandler)
