"""
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/1 22:25
@Software: PyCharm
@File    : CoverageShow.py
"""
import logging
import os
import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, Http404
from django.views import View
from minio.error import MinioException

from golang.lib import MinIoHandlers
from golang.lib.get_diff import GetIncrementCode, check_in_out, get_code_rownum
from golang.models import Report, Subassembly, Project
from golang.lib.goc import GocTool
from config.conf import gocconfig, minioconfig
from golang.lib.ParseHtml import Parsehtml

logger = logging.getLogger("django")


def search(path, name):
    """
    查找本地文件
    :param path:
    :param name:
    :return:
    """
    num = 0
    while True:
        for root, dirs, files in os.walk(path):  # path 为根目录
            if name in dirs or name in files:
                return True
        if num == 5:
            return False
        num += 1
        time.sleep(1)


class Coverageshow(View):
    def get(self, request, *args, **kwargs):
        ReportList = Report.objects.all().order_by("-CreateTime")
        project_list = Project.objects.all()
        return render(request, 'golang/CoverageShow.html', locals())


class CoverageTotal(View):
    def get(self, request, *args, **kwargs):
        subassembly_list = Subassembly.objects.all()
        return render(request, "golang/CoverageTotal.html", locals())

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        logger.info("请求包数据:%s" % data)
        checkparam = self.CheckParam(data=data)
        logger.info("参数校验:%s" % checkparam)
        if checkparam:
            subassemblyid = data.get("subassembly")
            version = data.get("version")
            gocaddress = data.get("gocaddress")
            subassembly = Subassembly.objects.get(pk=subassemblyid)
            covname = '.'.join([subassembly.SNameEN, "cov"])
            htmlname = '.'.join([subassembly.SNameEN, "html"])
            reportName = ".".join(
                ["_".join([subassembly.SNameEN, version, datetime.now().strftime("%Y%m%d%H%M%S")]), "html"])
            # 获取实时覆盖度数据cov 并保存至 codepath路径下
            logger.info("获取实时覆盖度数据cov 并保存至 codepath路径下")
            isgetcov = GocTool(path=gocconfig.gocpath, center=gocconfig.gocserver).getprofile(
                codepath=subassembly.CodePath,
                address=gocaddress, covname=covname)
            logger.info("获取实时覆盖度数据cov状态:%s" % isgetcov)
            if isgetcov:
                # 执行命令 生成html报告
                logger.info("执行命令 生成html报告")
                isgethtml = GocTool(path=gocconfig.gocpath, center=gocconfig.gocserver).gethtml(
                    codepath=subassembly.CodePath,
                    covname=covname, htmlname=htmlname)
                logger.info("执行命令 生成html报告:%s" % isgethtml)
                if isgethtml:
                    # 将报告上传至minio中
                    logger.info("将报告上传至minio中")
                    minio = MinIoHandlers.minioHandler(endpoint=minioconfig.MinIOUrl,
                                                       access_key=minioconfig.MinIOAccessKey,
                                                       secret_key=minioconfig.MinIOSecertKey)
                    minio.fputObject(bucketname=minioconfig.MinIOBucket, objectname=reportName,
                                     file=os.path.join(subassembly.CodePath, htmlname))
                    # 格式化 html，生成新的html

                    # 将新的 html上传至 minio中

                    # 获取覆盖度数据
                    coverage = Parsehtml(file=os.path.join(subassembly.CodePath, htmlname)).getCovAvg()
                    logger.info("获取覆盖度数据:%s" % coverage)
                    # report数据入库
                    report = Report.objects.create(RName=reportName, Subassembly=subassembly, Rtype=1, RVersion=version,
                                                   RoldUrl=reportName, CoverageAvg=coverage)
                    logger.info(
                        f"report保存:RName={reportName}, Subassembly={subassembly.SNameEN}, Rtype=1, RVersion={version},RoldUrl={reportName}, CoverageAvg={coverage}")

                    # 删除 本地数据 .cov .html

                    rmcov = GocTool(path=gocconfig.gocpath, center=gocconfig.gocserver).removefile(
                        codepath=subassembly.CodePath, filename=covname)
                    rmhtml = GocTool(path=gocconfig.gocpath, center=gocconfig.gocserver).removefile(
                        codepath=subassembly.CodePath, filename=htmlname)
                    logger.info("删除本地cov文件:%s" % rmcov)
                    logger.info("删除本地html文件:%s" % rmhtml)

                    return redirect("golang:coverageshow")
            return redirect('golang:coveragetotal')
        return redirect('golang:coveragetotal')

    def CheckParam(self, data):
        """
        参数校验
        :param data:
        :return:
        """
        subassemblyid = data.get("subassembly", None)
        version = data.get("version", None)
        gocaddress = data.get("gocaddress", None)
        if subassemblyid and version and gocaddress:
            for key, value in data.items():
                if value == "":
                    logger.info("param[%s]:%s, 参数校验值为空" % (key, value))
                    return False
            return True
        return False


class ReportShow(View):
    def get(self, request, id, *args, **kwargs):
        # return render(request, 'golang/CoverageDetail.html')
        report = Report.objects.get(pk=id)
        subassembly = Subassembly.objects.get(id=report.SubassemblyID_id)
        minio = MinIoHandlers.minioHandler(endpoint=subassembly.MinIOUrl, access_key=subassembly.MinIOAccessKey,
                                           secret_key=subassembly.MinIOSecertKey)
        try:
            data = minio.getObject(bucketname=subassembly.MinIOBucket, objectname=report.RName)
            logger.info("查看报告: %s" % report.RName)
            return HttpResponse(data.read())
        except MinioException as E:
            logger.error("MinioException:%s" % E)
            raise Http404("报告不存在")


class CoverageIncrement(View):
    def get(self, request, *args, **kwargs):
        subassembly_list = Subassembly.objects.all()
        project_list = Project.objects.all()
        return render(request, "golang/CoverageIncrement.html", locals())

    def post(self, request, *args, **kwargs):
        data = request.POST
        checkparam = self.CheckParam(data)
        if checkparam:
            subassemblyid = data.get("subassembly")
            version = data.get("version")
            coveragefile = data.get("coveragefile")
            startcommitid = data.get("startcommitid")
            endcommitid = data.get("endcommitid")
            subassembly = Subassembly.objects.get(id=subassemblyid)
            reportName = '-'.join(
                [str(subassembly.SNameEN), str(version), time.strftime('%Y%m%d%H%M%S', time.localtime())])
            # 下载cov文件
            minio = MinIoHandlers.minioHandler(endpoint=subassembly.MinIOUrl, access_key=subassembly.MinIOAccessKey,
                                               secret_key=subassembly.MinIOSecertKey)
            minio.fgetObject(bucketname=subassembly.MinIOBucket, objectname=coveragefile,
                             filepath=os.path.join(subassembly.GitPath, coveragefile))

            # 执行git diff 获取增量代码信息
            get_increment = self.Get_incrementCode(gitpath=subassembly.GitPath,
                                                   incrementfilename='.'.join([reportName, 'cov']),
                                                   startid=startcommitid, endid=endcommitid)
            logger.info("get_increment: %s" % get_increment)
            # 增量代码信息 与 覆盖度文件对比 获取增量代码的覆盖度
            # 增量代码覆盖度 保存成文件

            self.Get_incrementCov(change_code_rownum_list=get_increment,
                                  coverage=os.path.join(subassembly.GitPath, coveragefile),
                                  outfile=os.path.join(subassembly.GitPath, '.'.join([reportName, 'cov'])))
            # 增量代码覆盖度 执行os命令，生成报告
            # 执行os命令 生成HTML
            logger.info(
                "执行os命令生成HTML:cd %s;go tool cover -html=%s -o %s" % (
                    subassembly.GitPath, '.'.join([reportName, 'cov']), '.'.join([reportName, 'html'])))
            osresult = os.popen(
                'cd %s;go tool cover -html=%s -o %s' % (
                    subassembly.GitPath, '.'.join([reportName, 'cov']), '.'.join([reportName, 'html'])))
            # 上传html文件至 minio
            checkfileExist = search(path=subassembly.GitPath, name='.'.join([reportName, 'html']))
            logger.info("html生成: %s" % checkfileExist)
            if checkfileExist:
                logger.info("html文件上传minio:目录:%s;报告名:%s;本地文件路径:%s" % (
                    subassembly.MinIOBucket, reportName, os.path.join(subassembly.GitPath, reportName)))
                minio.fputObject(bucketname=subassembly.MinIOBucket, objectname='.'.join([reportName, 'html']),
                                 file=os.path.join(subassembly.GitPath, '.'.join([reportName, 'html'])))
                # minio.fputObject(bucketname=subassembly.MinIOBucket, objectname='.'.join([reportName, 'cov']),
                #                  file=os.path.join(subassembly.GitPath, '.'.join([reportName, 'cov'])))
                Report.objects.create(RName='.'.join([reportName, 'html']), SubassemblyID=subassembly,
                                      CoverageAvg='0', Rtype=2, RoldUrl='.'.join([reportName, 'html']),
                                      RVersion=version,
                                      RstartgitID=str(startcommitid)[0:8], RendgitID=str(endcommitid)[0:8])
                logger.info("记录报告:%s" % ('.'.join([reportName, 'html'])))
            try:
                self.Remove_File(os.path.join(subassembly.GitPath, coveragefile))
                self.Remove_File(os.path.join(subassembly.GitPath, '.'.join([reportName, 'html'])))
                self.Remove_File(os.path.join(subassembly.GitPath, '.'.join([reportName, 'cov'])))
                logger.info("删除文件成功-cov:[%s];报告文件:[%s]" % (coveragefile, reportName))
            except OSError as E:
                logger.error("文件不存在-cov:[%s];报告文件:[%s],报错:[%s]" % (coveragefile, reportName, E))
            return redirect('golang:coverageshow')
        return HttpResponse("param fail")

    def CheckParam(self, data):
        """
        参数校验
        :param data:
        :return:
        """
        subassemblyid = data.get("subassembly", None)
        version = data.get("version", None)
        startcommitid = data.get("startcommitid", None)
        endcommitid = data.get("endcommitid", None)
        coveragefile = data.get("coveragefile", None)
        if subassemblyid and version and startcommitid and endcommitid and coveragefile:
            for key, value in data.items():
                if value == "":
                    logger.info("param[%s]:%s, 参数校验值为空" % (key, value))
                    return False
            return True
        return False

    def Remove_File(self, file):
        try:
            os.remove(file)
        except OSError as E:
            logger.error("[%s]-文件不存在,报错:[%s]" % (file, E))
        return os.remove(file)

    def Get_incrementCode(self, gitpath, incrementfilename, startid, endid):
        # 判断增量文件是否存在，存在则删除，不存在，则在文件头添加相关参数
        logger.info("清除历史增量文件:%s" % os.path.join(gitpath, incrementfilename))
        if os.path.exists(os.path.join(gitpath, incrementfilename)):
            logger.info("清除历史增量文件:%s" % os.path.join(gitpath, incrementfilename))
            os.remove(os.path.join(gitpath, incrementfilename))
        logger.info("---写入增量文件头---")
        with open(os.path.join(gitpath, incrementfilename), "a+") as f:
            f.write("mode: count\n")
        logger.info("---写入增量文件头-完成--")
        get_increment = GetIncrementCode(git_path=gitpath)
        increment = get_increment.get_diff_log(start_commit_id=startid, end_commit_id=endid)
        logger.info("increment: %s" % increment)
        change_code_rownum_list = []
        for increment_code in increment:
            change_code_row_dict = {}
            change_code = increment_code["change_code"][0]
            file_path = increment_code["file_path"]
            if file_path[-2:] == "go":
                logger.info("increment_code: %s" % increment_code)
                start_num = increment_code["start_num"]
                end_num = increment_code["end_num"]
                # 获取增量代码的在文件中的行数 和 增量代码的列数
                if change_code.strip("\t") == "" or change_code.strip("\t") == "}" or change_code.strip(
                        "\t") == "{" or change_code.strip("\t")[0:2] == "//":
                    pass
                else:
                    change_code_rownum, change_code_columnNum = get_code_rownum(file=gitpath + file_path,
                                                                                start_num=start_num,
                                                                                end_num=end_num,
                                                                                check_code=change_code)
                    change_code_row_dict["file_path"] = file_path
                    change_code_row_dict["change_code_rownum"] = change_code_rownum
                    change_code_row_dict["change_code_columnNum"] = change_code_columnNum
                    change_code_rownum_list.append(change_code_row_dict)
            else:
                # print("@@ERROR:增量信息中未获取到.go文件")
                pass
        logger.info("change_code_rownum_list: %s" % change_code_rownum_list)
        return change_code_rownum_list

    def Get_incrementCov(self, change_code_rownum_list, coverage, outfile):
        logger.info("---与全量覆盖度数据做对比，保存增量覆盖度数据至文件中---")
        logger.info("%s - %s - %s" % (change_code_rownum_list, coverage, outfile))
        for row in change_code_rownum_list:
            file_path = row["file_path"]
            change_code_rownum = row["change_code_rownum"]
            change_code_columnNum = row["change_code_columnNum"]
            # 与全量覆盖度数据做对比，保存增量覆盖度数据至文件中
            check_in_out(complete_data=coverage, file=file_path, row=change_code_rownum, column=change_code_columnNum,
                         out_file=outfile)


class PrettyReport(View):
    def get(self, request):
        return render(request, 'golang/PrettyReport.html')
