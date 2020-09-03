#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Foo(object):

    def func(self, name):
        print(name)


obj = Foo()
# obj.func('wupeiqi') # 方法
print(obj.func)  # bound method

# obj = Foo()
# Foo.func(obj, '武沛齐') # 函数
print(Foo.func)  # function
