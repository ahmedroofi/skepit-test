from django.db import models
from users.models import User
# Create your models here.


class Folder(models.Model):
    """
    Folder Model
    """
    class Meta:
        verbose_name = "Folders"
        verbose_name_plural = "Folders"

    name = models.CharField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Document(models.Model):
    """
    Document Model
    """
    class Meta:
        verbose_name = "Documents"
        verbose_name_plural = "Documents"

    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_update = models.DateTimeField(auto_now=True)


class Topic(models.Model):
    """
    Topic Model
    """

    class Meta:
        verbose_name = "Topics"
        verbose_name_plural = "Topics"

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_update = models.DateTimeField(auto_now=True)
