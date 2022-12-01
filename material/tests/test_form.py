from ..forms import MaterialForm
from store.models import Store
from django.test import TestCase
from ..models import Material
from django.contrib.auth import get_user_model

User = get_user_model()

class MaterialFormTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'user', password = 'pass', email = 'e@mail.com')
        Store.objects.create(store_name = 'store', user = user)

    def test_form_save_item(self):
        store = Store.objects.get(store_name = 'store')
        form = MaterialForm(data = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 100, 'current_capacity': 50, "store": store})
        self.assertTrue(form.is_valid())

    def test_cannot_save_empty_item(self):
        form = MaterialForm(data = {})
        self.assertFalse(form.is_valid())

    def test_cannot_save_data_which_contains_current_capacity_larger_than_max_capacity(self):
        store = Store.objects.get(store_name = 'store')
        form = MaterialForm(data = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 100, 'current_capacity': 500, "store": store})
        self.assertFalse(form.is_valid())

    def test_initialize_form_validation_and_save_new_form_data(self):
        store = Store.objects.get(store_name = 'store')
        form = MaterialForm(initial = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 100, 'current_capacity': 50, "store": store})
        self.assertFalse(form.is_valid())
        form = MaterialForm(data = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 100, 'current_capacity': 50, "store": store})
        self.assertTrue(form.is_valid())

    def test_edit_form(self):
        store = Store.objects.get(store_name = 'store')
        material = Material.objects.create(material_name = 'material1', price =  1.5, max_capacity = 100, current_capacity = 50, store = store)
        initial_data = {
            "material_name": material.material_name, 
            'price': material.price, 
            'max_capacity': material.max_capacity, 
            'current_capacity': material.current_capacity, 
            "store": store
        }
        form = MaterialForm(initial = initial_data)
        form.fields['material_name'].widget.attrs['disabled'] = True
        form.fields['price'].widget.attrs['disabled'] = True
        form.fields['current_capacity'].widget.attrs['disabled'] = True

        data = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 200, 'current_capacity': 50, "store": store}
        form = MaterialForm(data = data, initial = initial_data)
        self.assertTrue(form.has_changed())
        form = MaterialForm(data, instance = material)
        self.assertTrue(form.is_valid())
        

