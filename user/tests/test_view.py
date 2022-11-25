from django.test import TestCase
from unittest import skip
from django.urls import reverse
from ..forms import (
    LoginForm, 
    INVALID_USERNAME_ERROR, INVALID_PASSWORD_ERROR, 
    INVALID_REPASSWORD_ERROR, INVALID_EMAIL_ERROR)

class UserLoginViewTest(TestCase):
    login_page_url = reverse('login_page')

    def test_user_able_to_browse_login_page(self):
        response = self.client.get(self.login_page_url) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_login_template_is_displayed(self):
        response = self.client.get(self.login_page_url)
        response_content = response.content.decode()
        # Check username is displayed
        self.assertIn('for="login-username"', response_content)
        self.assertIn('id="login-username"', response_content)
        # Check password is displayed
        self.assertIn('for="login-password', response_content)
        self.assertIn('id="login-password', response_content)
        # Check create new user link is displayed
        self.assertIn('id = "create-new-user-link"', response_content)
        # Check login button is displayed
        self.assertIn('class = "form-submit-button"', response_content)

    def test_login_template_using_form_template(self):
        response = self.client.get(self.login_page_url)
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_invalid_input_able_to_see_error(self):
        response = self.client.post(self.login_page_url, data = {'username': '', 'password': ''})
        self.assertIn('<div class = "error">', response.content.decode())

    def test_invalid_input_still_renders_login_template(self):
        response = self.client.post(self.login_page_url, data = {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

class CreateNewUserViewTest(TestCase):
    new_user_page_url = reverse("new_user_page")
    valid_username = "valid_username"
    valid_password = "valid_password"
    valid_repassword = valid_password
    valid_email = "valid@email.com"

    def post_data(self, username, password, repassword, email):
        return {
            "username": username,
            "password": password,
            "repassword": repassword,
            "email": email,
        }

    def post_valid_data(self):
        return self.client.post(
            self.new_user_page_url,
            data = self.post_data(
                self.valid_username, 
                self.valid_password,
                self.valid_repassword, 
                self.valid_email)
        )

    def test_create_new_user_template_is_displayed(self):
        response = self.client.get(self.new_user_page_url)
        response_content = response.content.decode()
        # Usename
        self.assertIn('for="new-username"', response_content)
        self.assertIn('id="new-username"', response_content)
        # Password
        self.assertIn('for="new-password"', response_content)
        self.assertIn('id="new-password"', response_content)
        # Re-password
        self.assertIn('for="new-repassword"', response_content)
        self.assertIn('id="new-repassword"', response_content)
        # Email
        self.assertIn('for="new-email"', response_content)
        self.assertIn('id="new-email"', response_content)

    def test_key_in_invalid_username_and_display_error(self):
        response = self.client.post(
            self.new_user_page_url, 
            data = self.post_data(
                '', self.valid_password, self.valid_repassword, self.valid_email
                )
            )
        self.assertIn(INVALID_USERNAME_ERROR, response.content.decode())

    def test_key_in_invalid_password_and_display_error(self):
        response = self.client.post(
            self.new_user_page_url, 
            data = self.post_data(
                self.valid_username, '', self.valid_repassword, self.valid_email
                )
            )
        self.assertIn(INVALID_PASSWORD_ERROR, response.content.decode())

    def test_key_in_invalid_repassword_and_display_error(self):
        response = self.client.post(
            self.new_user_page_url, 
            data = self.post_data(
                self.valid_username, self.valid_password, '', self.valid_email
                )
            )
        self.assertIn(INVALID_REPASSWORD_ERROR, response.content.decode())

    def test_key_in_invalid_email_and_display_error(self):
        response = self.client.post(
            self.new_user_page_url, 
            data = self.post_data(
                self.valid_username, self.valid_password, self.valid_repassword, ''
                )
            )
        self.assertIn(INVALID_EMAIL_ERROR, response.content.decode())

    def test_show_success_message_after_successfully_create_new_account(self):
        response = self.post_valid_data()
        self.assertIn('id="success-messages"', response.content.decode())