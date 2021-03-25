'''
-*- coding: utf-8 -*-
@Author  : cczhao2
@mail    : 907779487@qq.com
@Time    : 2021/3/24 13:58
@Software: PyCharm
@File    : forms.py
'''

from django import forms
from .models import Project, Subassembly


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["PName", "PNameEN", "Group"]
        widgets = {
            "PName": forms.TextInput(attrs={"class": "form-control", "placeholder": "如:统一账号平台"}),
            "PNameEN": forms.TextInput(attrs={"class": "form-control", "placeholder": "如:caccount"}),
            # "Group": forms.SelectMultiple(attrs={"class": "form-control custom-select"}),
            "Group": forms.Select(attrs={"class": "form-control custom-select"})
        }
        error_messages = {
            "PName": {"required": "此项必填"}
        }


class SubassemblyForm(forms.ModelForm):
    class Meta:
        model = Subassembly
        fields = ["SName", "SNameEN", "CodePath", "Project"]
        widgets = {
            "SName": forms.TextInput(attrs={"class": "form-control", "placeholder": "如:登录"}),
            "SNameEN": forms.TextInput(attrs={"class": "form-control", "placeholder": "如:login"}),
            "CodePath": forms.TextInput(attrs={"class": "form-control", "placeholder": "如:/data/code/login"}),
            "Project": forms.Select(attrs={"class": "form-control custom-select"}),
        }
        error_messages = {
            "SName": {"required": "此项必填"},
            "SNameEN": {"required": "此项必填"}
        }

    def clean_SNameEN(self):
        print(self.cleaned_data)
        SNameEN = self.cleaned_data['SNameEN']
        if Subassembly.objects.filter(SNameEN=SNameEN).exists():
            raise forms.ValidationError("组件标识重复")
        return SNameEN

