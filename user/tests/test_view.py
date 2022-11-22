from django.test import TestCase
from django.urls import reverse
# Create your tests here.
class UserLoginViewTest(TestCase):
    login_page_url = reverse('login_page')

    def test_user_able_to_browse_login_page(self):
        response = self.client.get(self.login_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_login_template_is_displayed(self):
        response = self.client.get(self.login_page_url)
        self.assertIn('id = "login-username', response.content.decode())
        self.assertIn('id = "login-button', response.content.decode())
