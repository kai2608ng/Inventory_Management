from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from ..models import Store

User = get_user_model()

class StoreModelTest(TestCase):
    def test_model_save_items(self):
        User.objects.create_user(username = 'username', password = 'password', email = 'some@email.com')
        user = User.objects.get(username = 'username')
        store1 = Store(store_name = "store1", user = user)
        store2 = Store(store_name = "store2", user = user)
        store1.save()
        store2.save()

    def test_user_cannot_save_same_store_name(self):
        user = User.objects.create_user(username = 'username', password = 'password', email = 'some@email.com')
        store1 = Store.objects.create(store_name = "store1", user = user)
        with self.assertRaises(IntegrityError):
            store2 = Store.objects.create(store_name = "store1", user = user)
    