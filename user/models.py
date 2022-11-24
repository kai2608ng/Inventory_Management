from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    class Meta:
        ordering = ["username"]

    username = models.CharField(max_length = 100, unique = True, null = False, primary_key = True)
    password = models.CharField(max_length = 100, null = False)
    email = models.EmailField(null = False)
    token = models.CharField(max_length = 255, default = str(uuid.uuid4()))

    def __str__(self):
        return self.username
