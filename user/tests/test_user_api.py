from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from typing import Any, Dict

# Not using Final, because no direct String is returned.
CREATE_USER_URL: str = reverse('user:create')
TOKEN_URL: str = reverse('user:token')
MANAGE_URL: str = reverse('user:manage')

def create_user(**params: Any) -> User:
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()

    def test_create_valid_user_success(self) -> None:
        """Test creating user with valid payload is successful"""
        payload: Dict[str, str] = {
            'email': 'abc@gmail.com',
            'password': '12345678',
            'name': 'sahil'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user: User = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self) -> None:
        """Test creating user that already exists"""
        payload: Dict[str, str] = {
            'email': 'abc@gmail.com',
            'password': '12345678',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self) -> None:
        """Test that the password must be more than 6 characters"""
        payload: Dict[str, str] = {
            'email': 'abc@gmail.com',
            'password': '12346'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists: User = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self) -> None:
        """Test that a token is created for a the user"""
        payload: Dict[str, str] = {
            'email': 'abc@gmail.com',
            'password': '12345678',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self) -> None:
        """Test that token is not created if invalid credentails are given"""
        create_user(email='abc@gmail.com', password='12345678')
        payload: Dict[str, str] = {'email': 'abc@gmail.com', 'password': '123458'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self) -> None:
        """Test that token is not created if user doesn't exist"""
        payload: Dict[str, str] = {'email': 'abc@gmail.com', 'passsword': '12345678'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self) -> None:
        """Test that email and password are required"""
        res = self.client.post(
            TOKEN_URL, {
                'email': 'abc@gmail.com',
                'password': ''
            })

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self) -> None:
        """Test that authenticate is required for users"""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authenticate"""

    def setUp(self) -> None:
        self.user: User = create_user(
            email='abc@gmail.com',
            password='12345678',
            name='name'
        )
        self.client: APIClient = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_method_not_allowed_on_manage_url(self):
        """Test that POST is not allowed on the manage url"""
        res = self.client.post(MANAGE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload: Dict[str, str] = {'name': 'test name', 'password': 'testpasword'}

        res = self.client.patch(MANAGE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
