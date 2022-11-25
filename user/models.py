from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False
