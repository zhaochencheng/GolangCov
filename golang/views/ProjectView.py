'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/1 20:15
@Software: PyCharm
@File    : ProjectView.py
'''
# from LoginProject import settings
import logging

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views import generic

from golang.forms import ProjectForm
from golang.models import Project

# Create your views here.
logger = logging.getLogger("django")


class ProjectShow(ListView):
    model = Project
    context_object_name = "ProjectList"
    template_name = "golang/projectShow.html"
    ordering = "-CreateTime"



class ProjectCreate(View):
    def get(self, request, *args, **kwargs):
        group_List = Group.objects.all()
        form = ProjectForm()
        return render(request, "golang/projectCreate.html", locals())

    def post(self, requst, *args, **kwargs):
        form = ProjectForm(requst.POST)
        if form.is_valid():
            print(form.cleaned_data)
            pname = form.cleaned_data.get("PName")
            pnameen = form.cleaned_data.get("PNameEN")
            group = form.cleaned_data.get("Group")
            project = Project.objects.create(PName=pname, PNameEN=pnameen, Group=group)
        return redirect('golang:projectshow')

class ProjectDelete(View):
    def get(self, request, id, *args, **kwargs):
        try:
            project = Project.objects.get(pk=id)
            logger.info("删除项目:%s" % project.PName)
            project.delete()
        except ObjectDoesNotExist as E:
            logger.error("ObjectDoesNotExist: %s" % E)
        return redirect('golang:projectshow')


