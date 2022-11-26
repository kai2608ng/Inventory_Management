from ..forms import StoreForm
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class StoreFormTest(TestCase):
    def test_form_save_item(self):
        User.objects.create_user(username = 'user', password = 'password', email = 'e@mail.com')
        user = User.objects.get(username = "user")
        form = StoreForm(data = {'store_name': "abc", 'user': user})
        form.save()