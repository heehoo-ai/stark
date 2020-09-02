#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools
from types import FunctionType

from django.conf.urls import url
from django.http import QueryDict
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.utils.pagination import Pagination
from django import forms


def get_choice_text(title, field):
    """
    对于Stark组件中定义列时，choice如果想要显示中文信息，调用此方法
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = "get_%s_display" % field
        return getattr(obj, method)()
    return inner


class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StarkHandler(object):
    display_list = []

    per_page_count = 10

    has_add_btn = True

    model_form_class = None

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"
        return DynamicModelForm

    def get_add_btn(self):
        if self.has_add_btn:
            return "<a class='btn btn-primary' href='%s'>添加</a>" % self.reverse_add_url()
        return None

    def display_edit(self, obj=None, is_header=False):
        if is_header:
            return "编辑"
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_change_url(pk=obj.pk))

    def display_del(self, obj=None, is_header=False):
        if is_header:
            return "删除"
        return mark_safe('<a href="%s">删除</a>' % self.reverse_delete_url(pk=obj.pk))

    def get_display_list(self):
        """
        获取页面上应该显示的列，预留的自定义扩展，例如根据用户的不同显示不同的列
        :return:
        """
        value = []
        value.extend(self.display_list)
        return value

    def __init__(self, site, model_class, prev):
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None

    def changelist_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        self.request = request

        # ########## 1. 处理分页 ##########
        all_count = self.model_class.objects.all().count()
        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        data_list = self.model_class.objects.all()[pager.start:pager.end]

        # ########## 2. 处理表格 ##########
        display_list = self.get_display_list()
        # 2.1 处理表格的表头
        header_list = []
        if display_list:
            for key in display_list:
                if isinstance(key, FunctionType):
                    verbose_name = key(self, obj=None, is_header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(key).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)

        # 2.2 处理表的内容
        body_list = []
        for row in data_list:
            tr_list = []
            if display_list:
                for key in display_list:
                    if isinstance(key, FunctionType):
                        tr_list.append(key(self, row, is_header=False))
                    else:
                        tr_list.append(getattr(row, key))
            else:
                tr_list.append(row)
            body_list.append(tr_list)

        ############## 3. 添加按钮   ################
        add_btn = self.get_add_btn()
        return render(
            request,
            'stark/changelist.html',
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn,
            }
        )

    def save(self, form, is_update=False):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param form:
        :param is_update:
        :return:
        """
        form.save()

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'stark/change.html', {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def change_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """
        current_change_object = self.model_class.objects.filter(pk=pk).first()
        if not current_change_object:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class(instance=current_change_object)
            return render(request, 'stark/change.html', {'form': form})
        form = model_form_class(data=request.POST, instance=current_change_object)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        origin_list_url = self.reverse_list_url()
        if request.method == 'GET':
            return render(request, 'stark/delete.html', {'cancel': origin_list_url})

        self.model_class.objects.filter(pk=pk).delete()
        return redirect(origin_list_url)

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param,)
        return '%s_%s_%s' % (app_label, model_name, param,)

    @property
    def get_list_url_name(self):
        """
        获取列表页面URL的name
        :return:
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        获取添加页面URL的name
        :return:
        """
        return self.get_url_name('add')

    @property
    def get_change_url_name(self):
        """
        获取修改页面URL的name
        :return:
        """
        return self.get_url_name('change')

    @property
    def get_delete_url_name(self):
        """
        获取删除页面URL的name
        :return:
        """
        return self.get_url_name('delete')

    def reverse_list_url(self):
        """
        跳转回列表页面时，生成URL
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name,)
        base_url = reverse(name)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return "%s?%s" % (base_url, param,)

    def reverse_add_url(self):
        """
        # 根据别名反向生产URL,使URL带有记忆功能，包含之前搜索条件
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_add_url_name)
        base_url = reverse(name)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def reverse_delete_url(self, *args, **kwargs):
        """
        # 根据别名反向生产URL,使URL带有记忆功能，包含之前搜索条件
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_delete_url_name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def reverse_change_url(self, *args, **kwargs):
        """
        # 根据别名反向生产URL,使URL带有记忆功能，包含之前搜索条件
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_change_url_name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)
        return inner

    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            url(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            url(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            url(r'^delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def extra_urls(self):
        return []


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """

        :param model_class: 是models中的数据库表对应的类。 models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :param prev: 生成URL的前缀
        :return:
        """
        """
        self._registry = [
            {'prev':None, 'model_class':models.Depart,'handler': DepartHandler(models.Depart,prev)对象中有一个model_class=models.Depart   },
            {'prev':'private', 'model_class':models.UserInfo,'handler':  StarkHandler(models.UserInfo,prev)对象中有一个model_class=models.UserInfo   }
            {'prev':None, 'model_class':models.Host,'handler':  HostHandler(models.Host,prev)对象中有一个model_class=models.Host   }
        ]
        """
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append(
            {'model_class': model_class, 'handler': handler_class(self, model_class, prev), 'prev': prev})

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            if prev:
                patterns.append(url(r'^%s/%s/%s/' % (app_label, model_name, prev,), (handler.get_urls(), None, None)))
            else:
                patterns.append(url(r'%s/%s/' % (app_label, model_name,), (handler.get_urls(), None, None)))

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
