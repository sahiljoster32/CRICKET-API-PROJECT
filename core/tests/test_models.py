from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import User


class ModelTests(TestCase):

    def test_create_a_user_with_email_successful(self) -> None:
        """Test creating a new user with an email is successful"""
        email = "abc@gmail.com"
        password = "12345678"
        user: User = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self) -> None:
        """Test the email for a new user is normalized"""
        email = 'abc@GMAIL.com'
        user: User = get_user_model().objects.create_user(email, '12345678')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self) -> None:
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '12345678')

    def test_create_new_superuser(self) -> None:
        """Test creating a new superuser"""
        user: User = get_user_model().objects.create_superuser(
            'abc@gmail.com',
            '12345678'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
