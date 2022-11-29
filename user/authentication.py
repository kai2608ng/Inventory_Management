from django.contrib.auth.backends import BaseBackend
from .models import Token

class TokenBackend(BaseBackend):
    def authenticate(self, request, token = None):
        try:
            user = Token.objects.get(key = token).user
        except Token.DoesNotExist:
            return None

        return user

    def get_item(self, token):
        try:
            return Token.objects.get(key = token).user
        except Token.DoesNotExist:
            return None