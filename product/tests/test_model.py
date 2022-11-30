from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Product
from store.models import Store
from django.db.utils import IntegrityError

User = get_user_model()
# Create your tests here.
class ProductModelTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username = "user1", password = 'pass1', email = 'e@mail.com')
        user2 = User.objects.create_user(username = "user2", password = 'pass2', email = 'e@mail.com')
        Store.objects.create(store_name = "store1", user = user1)
        Store.objects.create(store_name = "store2", user = user2)

    def test_product_save_item(self):
        user = User.objects.get(username = "user1")
        store = Store.objects.get(user = user)
        Product.objects.create(product_name = "product1", store = store)
        Product.objects.create(product_name = "product2", store = store)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_cannot_save_same_product(self):
        user = User.objects.get(username = "user1")
        store = Store.objects.get(user = user)
        Product.objects.create(product_name = "product1", store = store)
        with self.assertRaises(IntegrityError):
            Product.objects.create(product_name = "product1", store = store)

    def test_obtain_product_of_store(self):
        user = User.objects.get(username = "user1")
        store = Store.objects.get(user = user)
        Product.objects.create(product_name = "product1", store = store)
        Product.objects.create(product_name = "product2", store = store)
        Product.objects.create(product_name = "product3", store = store)
        store = Store.objects.get(user = user)
        products = store.product_entries.all()
        self.assertEqual(products.count(), 3)

    def test_save_same_item_but_different_store(self):
        user1 = User.objects.get(username = "user1")
        user2 = User.objects.get(username = "user2")
        store1 = Store.objects.get(user = user1)
        store2 = Store.objects.get(user = user2)
        Product.objects.create(product_name = "product", store = store1)
        Product.objects.create(product_name = "product", store = store2)
        self.assertEqual(Product.objects.all().count(), 2)


