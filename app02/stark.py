#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse
from stark.service.v1 import site, StarkHandler, Option, get_choice_text
from app02 import models


class HostHandler(StarkHandler):
    list_display = [StarkHandler.display_checkbox,  # 批量删除操作选择框
                    'id',  # 字段
                    'host', 'ip',
                    StarkHandler.display_edit,  # 添加编辑按钮
                    StarkHandler.display_del]  # 添加删除按钮
    action_list = [StarkHandler.action_multi_delete, ]
    search_list = ['host__contains', 'ip__contains']

    action_list = [StarkHandler.action_multi_delete, ]

site.register(models.Host, HostHandler)

site.register(models.Role)


class ProjectHandler(StarkHandler):
    search_list = ['title__contains', 'sever__contains', 'status__contains']
    # 定制页面显示的列
    list_display = [StarkHandler.display_checkbox,           # 批量删除操作选择框
                    'title',                                  # 字段
                    get_choice_text('状态', 'status'),        # 选择项字段
                    'server',
                    StarkHandler.display_edit,               #  添加编辑按钮
                    StarkHandler.display_del]                #  添加删除按钮
    action_list = [StarkHandler.action_multi_delete, ]
    search_group = [
        Option('status', is_multi=True),
        Option('server', db_condition={'id__gt': 0}),

    ]
site.register(models.Project, ProjectHandler)

