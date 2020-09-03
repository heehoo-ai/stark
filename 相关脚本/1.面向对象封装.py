#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Foo(object):

    def __init__(self, name):
        self.name = name

    def show_detail(self):
        """
        显示详细信息
        :return:
        """
        msg = "我叫%s，来自于地球。" % self.name
        print(msg)


obj1 = Foo('alex')
obj2 = Foo('武沛齐')
obj3 = Foo('珊珊')

obj1.show_detail()  # 我叫alex，来自地球。
obj2.show_detail()  # 我叫武沛齐，来自地球。
obj3.show_detail()  # 我叫珊珊，来自地球。
