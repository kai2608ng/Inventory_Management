from django.test import TestCase
from ..models import Material, MaterialQuantity
from product.models import Product
from store.models import Store
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.db import transaction

User = get_user_model()

class MaterialModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'user', password = 'pass', email = 'e@mail.com')
        Store.objects.create(store_name = "store1", user = user)

    def test_model_save_items(self):
        store = Store.objects.get(store_name = "store1")
        Material.objects.create(material_name = "material1", price = 1.5, store = store, max_capacity = 100, current_capacity = 50)
        Material.objects.create(material_name = "material2", price = 1.5, store = store, max_capacity = 100, current_capacity = 50)
        self.assertEqual(Material.objects.all().count(), 2)

    def test_model_cannot_save_without_price(self):
        store = Store.objects.get(store_name = "store1")
        with self.assertRaises(IntegrityError):
            Material.objects.create(material_name = "material1", store = store, max_capacity = 100, current_capacity = 50)

    def test_model_cannot_save_item_without_store(self):
        with self.assertRaises(IntegrityError):
            Material.objects.create(material_name = "material1", price = 1.5, max_capacity = 100, current_capacity = 50)

    def test_model_save_item_without_max_capacity(self):
        store = Store.objects.get(store_name = "store1")
        Material.objects.create(material_name = "material1", price = 1.5, store = store, current_capacity = 50)
        self.assertEqual(Material.objects.all().count(), 1)

    def test_model_save_item_without_current_capacity(self):
        store = Store.objects.get(store_name = "store1")
        Material.objects.create(material_name = "material1", price = 1.5, store = store, max_capacity = 100)
        self.assertEqual(Material.objects.all().count(), 1)
    
    def test_model_cannot_save_same_material_in_same_store(self):
        store = Store.objects.get(store_name = "store1")
        Material.objects.create(material_name = "material1", price = 1.5, store = store, max_capacity = 100, current_capacity = 50)
        with self.assertRaises(IntegrityError):
            Material.objects.create(material_name = "material1", price = 1.5, store = store, max_capacity = 100, current_capacity = 50)

class MaterialQuantityTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'user', password = 'pass', email = 'e@mail.com')
        Store.objects.create(store_name = "store1", user = user)

    def test_model_save_items(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        material1 = Material.objects.create(material_name = "material1", price = 1.5, store = store)
        material2 = Material.objects.create(material_name = "material2", price = 1.5, store = store)
        material3 = Material.objects.create(material_name = "material3", price = 1.5, store = store)
        MaterialQuantity.objects.create(product = product, material = material1, quantity = 5)
        MaterialQuantity.objects.create(product = product, material = material2, quantity = 5)
        MaterialQuantity.objects.create(product = product, material = material3, quantity = 5)
        self.assertEqual(MaterialQuantity.objects.all().count(), 3)

    def test_cannot_save_same_product_and_same_material(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        material = Material.objects.create(material_name = "material1", price = 1.5, store= store)
        MaterialQuantity.objects.create(product = product, material = material, quantity = 5)

        with self.assertRaises(IntegrityError):
            MaterialQuantity.objects.create(product = product, material = material, quantity = 5)

    def test_save_model_using_material_id(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        Material.objects.create(material_name = "material1", price = 1.5, store= store)
        with self.assertRaises(ValueError):
            MaterialQuantity.objects.create(product = product, material = 1, quantity = 5)

    def test_save_model_with_duplicated_product_but_the_first_is_saved(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        material = Material.objects.create(material_name = "material1", price = 1.5, store= store)
        MaterialQuantity.objects.create(product = product, material = material, quantity = 5)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MaterialQuantity.objects.create(product = product, material = material, quantity = 5)
        
        self.assertEqual(MaterialQuantity.objects.all().count(), 1)

    def test_obtain_material_from_product_id(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        material1 = Material.objects.create(material_name = "material1", price = 1.5, store= store)
        material2 = Material.objects.create(material_name = "material2", price = 1.5, store= store)
        MaterialQuantity.objects.create(product = product, material = material1, quantity = 5)
        MaterialQuantity.objects.create(product = product, material = material2, quantity = 5)
        print(MaterialQuantity.objects.filter(product__id = product.id))

    def test_verify_whether_product_can_be_sold(self):
        store = Store.objects.get(store_name = "store1")
        product = Product.objects.create(product_name = "product1", store = store)
        material1 = Material.objects.create(material_name = "material1", price = 1.5, store= store, max_capacity = 100, current_capacity = 50)
        material2 = Material.objects.create(material_name = "material2", price = 1.5, store= store, max_capacity = 100, current_capacity = 50)
        MaterialQuantity.objects.create(product = product, material = material1, quantity = 5)
        MaterialQuantity.objects.create(product = product, material = material2, quantity = 5)
        MaterialQuantity.objects.create(product = product, material = material2, quantity = 5)


