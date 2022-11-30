from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import ProductForm
from ..models import Product
from store.models import Store

User = get_user_model()

class ProductFormTest(TestCase):
    def test_save_item_with_form(self):
        user = User.objects.create(username = 'user', password = 'pass', email = 'e@mail.com')
        store = Store.objects.create(store_name = 'store', user = user)
        form = ProductForm(data = {'product_name': "product1", 'store': store})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Product.objects.all().count(), 1)

    def test_invalid_item_wont_be_saved(self):
        form = ProductForm(data = {'product_name': ''})
        self.assertFalse(form.is_valid())
            