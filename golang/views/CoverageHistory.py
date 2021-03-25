'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/1 22:25
@Software: PyCharm
@File    : CoverageHistory.py
'''

from django.shortcuts import render
from django.views import View


class CoverageHistory(View):
    def get(self, request, *args, **kwargs):
        return render(request, "golang/CoverageShow.html", locals())
