'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/24 17:06
@Software: PyCharm
@File    : Gocinfo.py
'''
from django.views import View
from django.views import generic
from golang.models import Subassembly
from golang.lib.goc import GocTool
from config.conf import gocconfig
from django.http.response import JsonResponse


class GocList(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        id = request.GET.get("id")
        # goc = GocTool(path=gocconfig.gocpath, center=gocconfig.gocserver)
        # golist = goc.goclist()
        golist = {"login": ["http://172.31.114.19:16567","http://172.31.114.19:36562"], "logout": ["http://172.31.114.19:12515"]}
        try:
            subassembly = Subassembly.objects.get(pk=id)
            # print(subassembly)
        except Subassembly.DoesNotExist:
            return JsonResponse([], safe=False)
        # print(golist.get(subassembly.SNameEN, []))
        return JsonResponse(golist.get(subassembly.SNameEN, []), safe=False)
