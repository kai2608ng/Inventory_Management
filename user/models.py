from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "User"
        ordering = ["pk"]

    email = models.EmailField(null = False, blank = False)
