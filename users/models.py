from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    Custom User Models
    """
    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
