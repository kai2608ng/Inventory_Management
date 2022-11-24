from ..models import User
from django.test import TestCase
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):
    def test_model_save_item(self):
        user1 = User(username = "username1", password = "password1", email = "email1@example.com")
        user1.save()

        user2 = User(username = "username2", password = "password2", email = "email2@example.com")
        user2.save()

        all_user = User.objects.all()
        self.assertEqual(all_user.count(), 2)
        self.assertEqual(all_user[0].username, user1.username)
        self.assertEqual(all_user[1].username, user2.username)

    def test_model_cannot_save_empty_item(self):
        user = User()
        with self.assertRaises(ValidationError):
            user.save()
            user.full_clean()