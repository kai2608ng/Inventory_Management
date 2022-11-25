from ..models import User, Token
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_model_save_item(self):
        user1 = User.objects.create_user(username = "username1", password = "password1", email = "email1@example.com")
        user1.save()

        user2 = User.objects.create_user(username = "username2", password = "password2", email = "email2@example.com")
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

class TokenModelTest(TestCase):
    def test_token_only_save_one_token_for_each_user(self):
        user1 = User.objects.create_user(username = "username1", password = "password1", email = "email1@example.com")
        with self.assertRaises(IntegrityError):
            token2 = Token.objects.create(user = user1)

    def test_token_was_created_after_creating_account(self):
        user1 = User.objects.create_user(username = "username1", password = "password1", email = "email1@example.com")
        token = Token.objects.get(user = user1).key