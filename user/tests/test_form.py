from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..forms import (
    LoginForm, NewUserForm, 
    INVALID_USERNAME_ERROR, INVALID_PASSWORD_ERROR)
from ..models import User
from unittest import skip

class BaseFormTest(TestCase):
    valid_username = "valid_username"
    valid_password = "valid_password"
    valid_repassword = valid_password
    valid_email = "valid@email.com"

    invalid_password = ''
    invalid_username = ''
    not_in_db_username = "not_in_db_username"
    not_in_db_password = "not_in_db_password"

    # NewUserTest
    def key_in_data(self, username, password, repassword, email):
        return {
            "username": username,
            "password": password,
            "repassword": repassword,
            "email": email,
        }

@skip
class LoginFormTest(BaseFormTest):
    def test_login_template(self):
        form = LoginForm(data = {'username': self.valid_username, 'password': self.valid_password})
        form_content = form.as_p()
        # Check username is displayed
        self.assertIn('for="login-username', form_content)
        self.assertIn('id="login-username', form_content)
        # Check password is displayed
        self.assertIn('for="login-password', form_content)
        self.assertIn('id="login-password', form_content)

    def test_key_in_invalid_username_to_login_form(self):
        form = LoginForm(data = {'username': self.invalid_username, 'password': self.valid_password})
        self.assertIn(INVALID_USERNAME_ERROR, form.as_p())

    def test_key_in_invalid_password_to_login_form(self):
        form = LoginForm(data = {'username': self.valid_username, 'password': self.invalid_password})
        self.assertIn(INVALID_PASSWORD_ERROR, form.as_p())

    @skip
    def test_key_in_username_and_password_database_does_not_exists(self):
        form = LoginForm(data = {'username': self.not_in_db_username, 'password': self.not_in_db_password})

        with self.assertRaises(ObjectDoesNotExist) as e:
            User.objects.get(pk = self.not_in_db_username)

        self.assertIn(INVALID_USERNAME_ERROR, form.as_p())

    @skip
    def test_valid_input_able_to_save_in_login_form(self):
        form = LoginForm(data = {'username': 'sky2608ng'})
        new_item = form.save()
        print(new_item)

class NewUserFormTest(BaseFormTest):
    def test_cannot_save_empty_form(self):
        form = NewUserForm()
        self.assertFalse(form.is_valid())

    def test_cannot_save_empty_username(self):
        form = NewUserForm(
            data = self.key_in_data('', self.valid_password, self.valid_repassword, self.valid_email)
        )
        self.assertFalse(form.is_valid())

    def test_cannot_save_empty_password(self):
        form = NewUserForm(
            data = self.key_in_data(self.valid_username, '', self.valid_repassword, self.valid_email)
        )
        self.assertFalse(form.is_valid())

    def test_cannot_save_empty_repassword(self):
        form = NewUserForm(
            data = self.key_in_data(self.valid_username, self.valid_password, '', self.valid_email)
        )
        self.assertFalse(form.is_valid())

    def test_cannot_save_empty_email(self):
        form = NewUserForm(
            data = self.key_in_data(self.valid_username, self.valid_password, self.valid_repassword, '')
        )
        self.assertFalse(form.is_valid())

    def test_able_to_save_valid_data(self):
        form = NewUserForm(
            data = self.key_in_data(
                 self.valid_username,
                 self.valid_password,
                 self.valid_repassword,
                 self.valid_email,
            )
        )
        self.assertTrue(form.is_valid())

    def test_item_saved_within_database(self):
        form = NewUserForm(
            data = self.key_in_data(
                 self.valid_username,
                 self.valid_password,
                 self.valid_repassword,
                 self.valid_email,
            )
        )
        form.save()
        user = User.objects.all()
        self.assertGreater(user.count(), 0)
