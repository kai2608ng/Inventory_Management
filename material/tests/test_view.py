from django.test import TestCase
from user.models import User, Token
from store.models import Store
from product.models import Product
from ..models import Material

class MaterialBaseTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username = 'user1', password = 'password1', email = 'user1@email.com')
        user2 = User.objects.create_user(username = 'user2', password = 'password2', email = 'user2@email.com')
        store1 = Store.objects.create(store_name = 'store1', user = user1)
        Store.objects.create(store_name = 'store2', user = user2)
        Token.objects.create(user = user1)
        Token.objects.create(user = user2)
        Material.objects.create(material_name = "material1", price = '1.5', max_capacity = 50, current_capacity = 40, store = store1)
        Material.objects.create(material_name = "material2", price = '1.5', max_capacity = 50, current_capacity = 40, store = store1)

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

class MaterialViewTest(MaterialBaseTest):
    def test_browse_material_page(self):
        response = self.get_webpage('/user1/material/', 'user1', 'password1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'material/material.html')

class NewMaterialViewTest(MaterialBaseTest):
    def test_browse_new_material_page(self):
        response = self.get_webpage("/user1/new_material/", 'user1', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "material/new_material.html")

class EditMaterialViewTest(MaterialBaseTest):
    def test_browse_edit_material_page(self):
        response = self.get_webpage('/user1/edit_material/1/', 'user1', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "material/edit_material.html")

class DeleteMaterialViewTest(MaterialBaseTest):
    def test_browse_delete_material_page(self):
        response = self.get_webpage("/user1/delete_material/1/", 'user1', 'password')
        self.assertEqual(response.status_code, 302)

    def test_browse_item_deleted_page(self):
        response = self.get_webpage('/user1/material/', 'user1', 'password1')
        self.assertIn("material1", response.content.decode())
        self.get_webpage("/user1/delete_material/1/", 'user1', 'password')
        response = self.get_webpage('/user1/material/', 'user1', 'password1')
        self.assertNotIn("material1", response.content.decode())
        
