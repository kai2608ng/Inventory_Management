from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from ..models import Store

User = get_user_model()

class StoreModelTest(TestCase):
    def test_model_save_items(self):
        User.objects.create_user(username = 'username1', password = 'password', email = 'some@email.com')
        User.objects.create_user(username = 'username2', password = 'password', email = 'some@email.com')
        user1 = User.objects.get(username = 'username1')
        user2 = User.objects.get(username = 'username2')
        store1 = Store(store_name = "store1", user = user1)
        store2 = Store(store_name = "store2", user = user2)
        store1.save()
        store2.save()

    def test_user_cannot_save_same_store_name(self):
        user = User.objects.create_user(username = 'username', password = 'password', email = 'some@email.com')
        store1 = Store.objects.create(store_name = "store1", user = user)
        with self.assertRaises(IntegrityError):
            store2 = Store.objects.create(store_name = "store1", user = user)
    