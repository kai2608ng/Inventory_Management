from django.test import TestCase
from user.models import User, Token
from store.models import Store

class ProductBaseTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username = 'user1', password = 'password1', email = 'user1@email.com')
        user2 = User.objects.create_user(username = 'user2', password = 'password2', email = 'user2@email.com')
        Store.objects.create(store_name = 'store1', user = user1)
        Store.objects.create(store_name = 'store2', user = user2)
        Token.objects.create(user = user1)
        Token.objects.create(user = user2)

    def user_authentication(self, username, password):
        self.client.login(username = username, password = password)

        session = self.client.session
        session['token'] = Token.objects.get(user = User.objects.get(username = username)).key
        session.save()

    def get_webpage(self, path, username, password):
        self.user_authentication(username, password)
        return self.client.get(path)

    def post_webpage(self, path, username, password, data):
        self.user_authentication(username, password)
        return self.client.post(path, data = data)

class ProductViewTest(ProductBaseTest):
    def test_able_to_browse_product_page(self):
        response = self.get_webpage('/user1/product/', 'user1', 'password1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')

class NewProductViewTest(ProductBaseTest):
    def test_able_to_browse_new_product_page(self):
        response = self.get_webpage("/user1/new_product/", 'user1', 'password1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/new_product.html')

    def test_able_to_see_error_if_key_in_invalid_input(self):
        response = self.post_webpage(
            "/user1/new_product/", 
            'user1', 'password1', 
            data = {'product_name': ''})
        self.assertIn("error", response.content.decode())

    def test_able_to_see_new_product_if_key_in_valid_input(self):
        user = User.objects.get(username = "user1")
        store = Store.objects.get(user = user)
        response = self.post_webpage(
            "/user1/new_product/", 
            "user1", "password1", 
            data = {'product_name': 'product1', 'store': store})
        response = self.get_webpage(
            '/user1/product/',
            "user1", "password1")
        self.assertIn("product-detail-text", response.content.decode())
