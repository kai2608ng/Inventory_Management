from django.test import TestCase
from django.urls import reverse
from ..forms import LoginForm
# Create your tests here.
class UserLoginViewTest(TestCase):
    login_page_url = reverse('login_page')

    def test_user_able_to_browse_login_page(self):
        response = self.client.get(self.login_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_login_template_is_displayed(self):
        response = self.client.get(self.login_page_url)
        response_content = response.content.decode()
        self.assertIn('for = "login-username"', response_content)
        self.assertIn('id="login-username"', response_content)
        self.assertIn('id = "login-button"', response_content)

    def test_login_template_using_form_template(self):
        response = self.client.get(self.login_page_url)
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_invalid_input_able_to_see_error(self):
        response = self.client.post(self.login_page_url, data = {'username': ''})
        self.assertIn('<div class = "error">', response.content.decode())

    def test_invalid_input_renders_login_template(self):
        response = self.client.post(self.login_page_url, data = {'username': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")