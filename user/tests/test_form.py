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
    
    def test_valid_input_able_to_save_in_login_form(self):
        form = LoginForm(data = {'username': "sky2608ng"})
        new_item = form.save()
        print(new_item)