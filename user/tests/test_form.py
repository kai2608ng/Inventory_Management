from django.test import TestCase
from ..forms import LoginForm, INVALID_USERNAME_ERROR

class LoginFormTest(TestCase):

    def test_login_template(self):
        form = LoginForm()
        # label
        self.assertIn('for="login-username', form.as_p())
        # input_box
        self.assertIn('id="login-username', form.as_p())

    def test_login_key_in_invalid_data(self):
        form = LoginForm(data = {'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [INVALID_USERNAME_ERROR])
    