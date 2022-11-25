from django.test import TestCase
from django.urls import reverse

class AuthenticationTest(TestCase):
    login_page_url = reverse("login_page")

    def test_user_and_password_does_not_exist(self):
        response = self.client.post(self.login_page_url, data = {'username': 'no_username', 'password': 'no_password'})
        self.assertNotIn("token", response.context)

