#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.service.v1 import site, StarkHandler, get_choice_text
from app01 import models


class DepartHandler(StarkHandler):
    display_list = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]

site.register(models.Depart, DepartHandler)


class UserInfoHandler(StarkHandler):

    # 定制页面显示的列
    display_list = ['name',
                    get_choice_text('性别', 'gender'),
                    'age', 'email', 'depart',
                    StarkHandler.display_edit,
                    StarkHandler.display_del]

    per_page_count = 1

    # def get_display_list(self):
    #
    #     return ['name', 'age']

site.register(models.UserInfo, UserInfoHandler)
