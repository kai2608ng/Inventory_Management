from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Store
from user.models import Token, User
from unittest import skip

User = get_user_model()

class StoreViewTest(TestCase):
    def setUp(self):
        user_has_store = User.objects.create_user(username = "user_has_store", password = 'password1', email = 'user1@email.com')
        user_does_not_have_store = User.objects.create_user(username = "user_does_not_have_store", password = 'password2', email = 'user2@email.com')
        Token.objects.create(user = user_has_store)
        Token.objects.create(user = user_does_not_have_store)
        Store.objects.create(store_name = "store1", user = user_has_store)

    def login(self, username, password):
        return self.client.post("/", data = {"username": username, "password": password})

    def user_authentication(self, username, password):
        user = User.objects.get(username = username)
        # User login
        self.client.login(username = username, password = password)
        # Token Authentication
        session = self.client.session
        session['token'] = Token.objects.get(user = user).key
        session.save()

    def get_webpage(self, path, username, password):
        self.user_authentication(username, password)
        return self.client.get(path)

class HomePageViewTest(StoreViewTest):
    def test_show_redirected_to_home_page(self):
        response = self.login("user_has_store", "password1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'user_has_store/home/')

    def test_not_authorized_user_to_login_page(self):
        response = self.client.get(f'/user_has_store/home/')
        self.assertRedirects(response, "/")

    def test_show_home_page(self):
        response = self.get_webpage(
            f"/user_has_store/home/", 
            "user_has_store", 
            "password1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/home.html")

    def test_display_store_of_the_user(self):
        response = self.get_webpage(
            f"/user_has_store/home/", 
            "user_has_store", 
            "password1")
        self.assertIn('user_has_store', response.content.decode())
        store = response.context['store']
        db_store = Store.objects.all()
        self.assertEqual(db_store.count(), store.count())

    def test_show_nothing_if_user_does_not_created_store(self):
        response = self.get_webpage(
            f"/user_does_not_have_store/home/", 
            "user_does_not_have_store", 
            "password2")
        self.assertIn("No Store found", response.content.decode())

class CreateNewStoreViewTest(StoreViewTest):
    def test_able_to_browse_new_store_page(self):
        response = self.get_webpage(
            "/user_does_not_have_store/new_store/", 
            "user_does_not_have_store", 
            "password2")
        self.assertTemplateUsed(response, 'store/new_store.html')
        self.assertEqual(response.status_code, 200)

    def test_show_empty_store_template(self):
        response = self.get_webpage(
            "/user_does_not_have_store/new_store/",
            "user_does_not_have_store",
            "password2")
        self.assertIn('for="store-name"', response.content.decode())
