'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/1 20:45
@Software: PyCharm
@File    : index.py
'''

from django.shortcuts import render


def index(request):
    return render(request, "golang/index.html", locals())
