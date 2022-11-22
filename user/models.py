from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    username = models.CharField(
        max_length = 100, unique = True, null = False, blank = False, 
        default = '', primary_key = True)
    token = models.CharField(max_length = 255, default = str(uuid.uuid4()))