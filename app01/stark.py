#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms

from stark.service.v1 import site, StarkHandler, get_choice_text, StarkModelForm
from app01 import models


class DepartHandler(StarkHandler):
    display_list = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
    has_add_btn = True

site.register(models.Depart, DepartHandler)


class UserInfoModelForm(StarkModelForm):

    classes = forms.CharField()  # 自定义数据库没有的字段
    class Meta:
        model = models.UserInfo
        fields = ['name', 'gender', 'age', 'email']   # 数据库中的depart字段没有在可编辑列表


class UserInfoHandler(StarkHandler):

    # 定制页面显示的列
    display_list = ['name',                                  # 字段
                    get_choice_text('性别', 'gender'),        # 选择项字段
                    'age', 'email', 'depart',
                    StarkHandler.display_edit,               #  添加编辑按钮
                    StarkHandler.display_del]                #  添加删除按钮

    per_page_count = 10    # 自定制每页显示的条数
    has_add_btn = True     #  # 自定制是否显示添加按钮

    model_form_class = UserInfoModelForm   # 如果需要添加数据库没有的字段，可用UserInfoModelForm类自定制

    def save(self, form, is_update=False):
        """
        用于自定义可编辑字段时，某些存在于数据库却没有在编辑页显示的字段，在这里进行默认赋值
        :param form:
        :param is_update:
        :return:
        """
        form.instance.depart_id = 1
        form.save()

site.register(models.UserInfo, UserInfoHandler)
