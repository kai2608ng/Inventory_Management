from django import forms
from .models import User

INVALID_USERNAME_ERROR = "Please enter a valid username"

class LoginForm(forms.models.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            "username": forms.TextInput(
                attrs = {
                    "placeholder": "Username",
                    "id": "login-username",
                    "name": "username",
                }
            )
        }
        error_messages = {
            "username": {"required": INVALID_USERNAME_ERROR}
        }