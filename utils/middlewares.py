'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/24 11:13
@Software: PyCharm
@File    : middlewares.py
'''
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status


class ResponseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_response(self, request, response):
        resp = {"code": "000000", "desc": "success"}
        if isinstance(response, Response):
            if response.status_code == 200 or response.status_code == 201:
                resp.update({"data": response.data})
            else:
                resp["code"] = "000001"
                resp["desc"] = "fail"
                resp.update({"errors": response.data})
            response.data = resp
            response.content = response.rendered_content
            return response
        return response


    def process_exception(self, request, exception):
        pass
