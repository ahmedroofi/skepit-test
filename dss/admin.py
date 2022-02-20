from django.contrib import admin
from dss.models import Folder, Document, Topic
# Register your models here.


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    ordering = ("-id",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    ordering = ("-id",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = ("id", "description")
    ordering = ("-id",)