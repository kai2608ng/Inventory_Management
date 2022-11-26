from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Store
from unittest import skip

User = get_user_model()

class StoreViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username = "user_has_store", password = 'password1', email = 'user1@email.com')
        user2 = User.objects.create_user(username = "user_does_not_have_store", password = 'password2', email = 'user2@email.com')
        Store.objects.create(store_name = "store1", user = user1)
        Store.objects.create(store_name = "store2", user = user1)
        self.client.force_login(user1)
        self.client.force_login(user2)

@skip
class HomePageViewTest(StoreViewTest):

    def test_show_home_page(self):
        response = self.client.get("/user_has_store/home/")
        self.assertEqual(response.status_code, 200)

    def test_display_store_of_the_user(self):
        response = self.client.get("/user_has_store/home/")
        self.assertIn('user', response.content.decode())
        store = response.context['store']
        db_store = Store.objects.all()
        self.assertEqual(db_store.count(), store.count())

    def test_show_store_if_user_has_created_store(self):
        response = self.client.get("/user_does_not_have_store/home/")
        print(response.context['store'].count())
        self.assertIn("No Store found", response.content.decode())

class CreateNewStoreViewTest(StoreViewTest):
    def test_able_to_browse_new_store_page(self):
        response = self.client.get("/user_does_not_have_store/new_store/")
        self.assertTemplateUsed(response, 'store/new_store.html')
        self.assertEqual(response.status_code, 200)

    def test_show_new_store_template(self):
        response = self.client.get("/user_does_not_have_store/new_store/")
        self.assertIn('id="store-name', response.content.decode())