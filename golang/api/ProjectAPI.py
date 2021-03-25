'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/22 21:09
@Software: PyCharm
@File    : ProjectAPI.py
'''

from rest_framework import generics

from golang.models import Project
from golang.serializers import ProjectSerializer


# class ProjectListView(views.APIView):
#     serializer_class = ProjectSerializer
#
#     def get(self, request, *args, **kwargs):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         result = Response(serializer.data)
#         return result
#
#     def post(self, request, *args, **kwargs):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = "id"
