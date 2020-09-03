#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Base(object):
    def __init__(self, name):
        self.name = name

    def show_detail(self):
        """
        显示详细信息
        :return:
        """
        msg = "我叫%s，来自于地球。" % self.name
        print(msg)


class Foo(Base):
    def show_detail(self):
        """
        显示详细信息
        :return:
        """
        msg = "我叫%s，来自于约球。" % self.name
        print(msg)


class Bar(Base):
    pass


obj1 = Foo('老男孩')
obj1.show_detail()

obj2 = Bar('alex')
obj2.show_detail()
