from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Project(models.Model):
    PName = models.CharField(verbose_name='项目名称', max_length=200)
    PNameEN = models.CharField(verbose_name='项目名称英文', max_length=200)
    Group = models.ForeignKey(to=Group, on_delete=models.DO_NOTHING)
    User = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    CreateTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更改时间', auto_now=True)

    def __str__(self):
        return self.PName

    class Meta:
        db_table = "project"
        ordering = ["id", "-CreateTime"]


class Subassembly(models.Model):
    SName = models.CharField(verbose_name='组件名', max_length=200)
    SNameEN = models.CharField(verbose_name='组件名英文', max_length=200)
    CodePath = models.CharField(verbose_name="git存储目录", max_length=400)
    # GitUrl = models.CharField(verbose_name='git地址', max_length=200, blank=True, null=True)
    # GitUsername = models.CharField(verbose_name='git登录用户名', max_length=200, blank=True, null=True)
    # GitPassword = models.CharField(verbose_name='git登录密码', max_length=200, blank=True, null=True)
    # MinIOUrl = models.CharField(verbose_name='MinIO地址', max_length=200)
    # MinIOAccessKey = models.CharField(verbose_name='MinIO登录用户名', max_length=200)
    # MinIOSecertKey = models.CharField(verbose_name='MinIO登录密码', max_length=200)
    # MinIOBucket = models.CharField(verbose_name="MinIO目录", max_length=200, blank=True, null=True)
    Project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    CreateTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.SName

    class Meta:
        db_table = "subassembly"
        ordering = ["-CreateTime"]


class Report(models.Model):
    RName = models.CharField(max_length=200, default="", verbose_name="报告名称")
    Subassembly = models.ForeignKey(to=Subassembly, on_delete=models.DO_NOTHING, default="")
    CoverageAvg = models.CharField(max_length=200, default="", verbose_name="覆盖率")
    # 1:全量 2:增量
    type_choice = (
        (1, "全量"),
        (2, "增量")
    )
    Rtype = models.IntegerField(default=1, verbose_name="报告类型", choices=type_choice)
    RVersion = models.CharField(max_length=200, verbose_name="版本号", blank=True, null=True)
    RstartgitID = models.CharField(max_length=200, verbose_name="git起始commitID", null=True, blank=True)
    RendgitID = models.CharField(max_length=200, verbose_name="git终止commitID", null=True, blank=True)
    RoldUrl = models.CharField(max_length=200, verbose_name="原生报告路径", null=True, blank=True)
    RnewUrl = models.CharField(max_length=200, verbose_name="新报告路径", null=True, blank=True)
    CreateTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = "report"
        ordering = ["id", "-CreateTime"]
