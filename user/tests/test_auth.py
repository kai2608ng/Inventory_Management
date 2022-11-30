from django.test import TestCase
from django.urls import reverse
from ..models import User, Token
from django.contrib.auth import authenticate

class AuthenticationTest(TestCase):
    login_page_url = reverse("login_page")

    def test_no_token_received_if_user_and_password_does_not_exist(self):
        response = self.client.post(self.login_page_url, data = {'username': 'no_username', 'password': 'no_password'})
        self.assertNotIn("token", self.client.session)
        self.assertTemplateUsed(response, "user/login.html")

    def test_token_is_created_when_login_to_valid_account(self):
        # Create a new user and store it in the database
        user = User.objects.create_user(username = "username1", password = "password1", email = "email1@example.com")
        self.assertEqual(User.objects.all().count(), 1)
        #
        response = self.client.post(reverse('login_page'), data = {'username': 'username1', 'password': 'password1'})
        self.assertRedirects(response, reverse("home_page", args = (user.username, )))
        token = Token.objects.get(user = user).key
        self.assertEqual(self.client.session['token'], token)