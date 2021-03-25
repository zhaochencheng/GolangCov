'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/22 21:06
@Software: PyCharm
@File    : serializers.py
'''
from rest_framework import serializers
from .models import Project, Subassembly
from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "PName", "PNameEN", "Group", "CreateTime")



class SubassemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subassembly
        fields = ("id", "SName", "SNameEN", "GitPath", "MinIOUrl", "ProjectID", "CreateTime")
