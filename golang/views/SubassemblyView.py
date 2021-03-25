'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/1 21:03
@Software: PyCharm
@File    : SubassemblyView.py
'''
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from golang.lib import MinIoHandlers
from golang.forms import SubassemblyForm

from golang.models import Subassembly

logger = logging.getLogger("django")


class SubassemblyShow(ListView):
    model = Subassembly
    context_object_name = "SubassemblyList"
    template_name = "golang/SubassemblyShow.html"




class SubassemblyCreate(View):
    def get(self, request, *args, **kwargs):
        form = SubassemblyForm()
        return render(request, "golang/SubassemblyCreate.html", locals())

    def post(self, request, *args, **kwargs):
        # 新增组件时，创建minio buckets
        form = SubassemblyForm(request.POST)
        if form.is_valid():
            sname = form.cleaned_data.get("SName")
            snameEN = form.cleaned_data.get("SNameEN")
            codepath = form.cleaned_data.get("CodePath")
            project = form.cleaned_data.get("Project")
            Subassembly.objects.create(SName=sname, SNameEN=snameEN, CodePath=codepath, Project=project)
            return redirect('golang:subassemblyshow')
                # project = Project.objects.get(pk=ProjectID)
                # sub = Subassembly(SName=SName, SNameEN=SNameEN, GitPath=GitPath, MinIOUrl=MinIOUrl,
                #                   MinIOAccessKey=MinIOAccessKey,
                #                   MinIOSecertKey=MinIOSecertKey, MinIOBucket=MinIOBucket, ProjectID=project)
                #
                # minio = MinIoHandlers.minioHandler(endpoint=MinIOUrl, access_key=MinIOAccessKey,
                #                                    secret_key=MinIOSecertKey)
                # bucketExist = minio.existBuckets(bucket_name=MinIOBucket)
                # if bucketExist:
                #     logger.info("MinIO中[%s]目录已存在" % MinIOBucket)
                # else:
                #     minio.makebucket(bucket_name=MinIOBucket)
                # sub.save()
        return render(request, "golang/SubassemblyCreate.html", locals())

    def CheckParam(self, data):
        '''
        参数校验
        :param data:
        :return:
        '''
        for key, value in data.items():
            if value == "":
                logger.info("param[%s]:%s, 参数校验值为空" % (key, value))
                return False
        if data.get("ProjectID") is None:
            logger.info("param[%s]:%s, 参数校验值为空" % ("ProjectID", data.get("ProjectID")))
            return False
        return True

    def CheckSnameEN(self, *args, **kwargs):
        findcount = Subassembly.objects.filter(SNameEN=kwargs.get("SNameEN"), ProjectID=kwargs.get("ProjectID")).count()
        if findcount:
            logger.info("在该项目id[%s]下已存在该[%s]组件标识" % (kwargs.get("ProjectID"), kwargs.get("SNameEN")))
            return False
        else:
            return True


class SubassemblyDelete(View):
    def get(self, request, id, *args, **kwargs):
        try:
            subassembly = Subassembly.objects.get(pk=id)
            logger.info("删除组件:%s" % subassembly.SName)
            subassembly.delete()
        except ObjectDoesNotExist as E:
            logger.error("ObjectDoesNotExist: %s" % E)
        return redirect('golang:subassemblyshow')
