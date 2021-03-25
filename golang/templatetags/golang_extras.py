'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/2 17:01
@Software: PyCharm
@File    : golang_extras.py
'''
from django import template

register = template.Library()

@register.filter(name="NoneToEmpty")
def None_to_empty(value):
    return "--" if value is None else value