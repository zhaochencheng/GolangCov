from django.contrib import admin

# Register your models here.
from .models import Project, Subassembly


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # pass
    list_display = ("PName", "PNameEN", "Group", "User", "CreateTime")

@admin.register(Subassembly)
class SubassemblyAdmin(admin.ModelAdmin):
    list_display = ("SName", "SNameEN")
