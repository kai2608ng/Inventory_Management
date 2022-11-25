from django import forms
from .models import User

INVALID_USERNAME_ERROR = "Please enter a valid username."
INVALID_PASSWORD_ERROR = "Please enter a valid password."
INVALID_REPASSWORD_ERROR = "Please enter same password."
INVALID_EMAIL_ERROR = "Please enter a valid email."

class LoginForm(forms.models.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs = {
                    "id": "login-username",
                    "name": "username"
                }
            ),
            "password": forms.PasswordInput(
                attrs = {
                    "id": "login-password",
                    "name": "password"
                }
            )
        }
        error_messages = {
            "username": {"required": INVALID_USERNAME_ERROR},
            "password": {"required": INVALID_PASSWORD_ERROR}
        }

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","password", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs = {
                    "id": "new-username",
                    "name": "username",
                }
            ),
            "password": forms.PasswordInput(
                attrs = {
                    "id": "new-password",
                    "name": "password"
                }
            ),
            "email": forms.EmailInput(
                attrs = {
                    "id": "new-email",
                    "name": "email"
                }
            )
        }
        error_messages = {
            "username": {"required": INVALID_USERNAME_ERROR},
            "password": {"required": INVALID_PASSWORD_ERROR},
            "email": {"required": INVALID_EMAIL_ERROR}
        }

    repassword = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "id": "new-repassword", 
                "name": "repassword"
            },
        ),
        error_messages = {
            "required": INVALID_REPASSWORD_ERROR
        },
        label = "Re-type Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repassword = cleaned_data.get("repassword")

        if password != repassword:
            error_messages = "Please key in same password"
            self.add_error("password", error_messages)
            self.add_error("repassword", error_messages)
    