from ..forms import MaterialForm
from django.test import TestCase

class MaterialFormTest(TestCase):
    def test_form_save_item(self):
        form = MaterialForm(data = {"material_name": 'material1', 'price': 1.5, 'max_capacity': 100, 'current_capacity': 50})
        self.assertTrue(form.is_valid())

    def test_cannot_save_empty_item(self):
        form = MaterialForm(data = {})
        self.assertFalse(form.is_valid())