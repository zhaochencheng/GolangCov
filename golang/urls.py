'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/22 21:13
@Software: PyCharm
@File    : urls.py
'''

from django.urls import path
from golang.api import ProjectAPI
from golang.views import index, ProjectView, SubassemblyView, CoverageHistory, CoverageShow, Gocinfo

app_name = "golang"

urlpatterns = [

    path("index/", index.index, name="index"),
    path("projectShow/", ProjectView.ProjectShow.as_view(), name="projectshow"),
    path("projectCreate/", ProjectView.ProjectCreate.as_view(), name="projectcreate"),
    path("project/delete/<int:id>/", ProjectView.ProjectDelete.as_view(), name="project_delete"),
    path("subassemblyShow/", SubassemblyView.SubassemblyShow.as_view(), name="subassemblyshow"),
    path("subassemblyCreate/", SubassemblyView.SubassemblyCreate.as_view(), name="subassemblycreate"),
    path("subassembly/delete/<int:id>/", SubassemblyView.SubassemblyDelete.as_view(), name="subassemblydelete"),
    path("coverageShow/", CoverageShow.Coverageshow.as_view(), name="coverageshow"),
    path("coverageTotal/", CoverageShow.CoverageTotal.as_view(), name="coveragetotal"),
    path('coverageIncrement/', CoverageShow.CoverageIncrement.as_view(), name="coverageincrement"),
    path("coverageTotal/<int:id>", CoverageShow.CoverageTotal.as_view(), name="coveragetotal"),
    # path("coverageHistory/", CoverageHistory.CoverageHistory.as_view(), name="coveragehistory"),
    path("coverageReport/<int:id>", CoverageShow.ReportShow.as_view(), name="coveragereport"),
    path("prettyReport/", CoverageShow.PrettyReport.as_view(), name="prettyreport"),

    path('goclist', Gocinfo.GocList.as_view(), name="goclist"),
]
