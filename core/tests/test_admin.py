from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import User


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client: Client = Client()
        self.admin_user: User = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='12345678'
        )
        self.client.force_login(self.admin_user)
        self.user: User = get_user_model().objects.create_user(
            email = 'abc@gmail.com',
            password = '12345678',
            name = 'test name'
        )

    def test_users_listed(self) -> None:
        """Test that user are listed on user page"""
        url: str = reverse('admin:core_user_changelist')
        res: str = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self) -> None:
        """Test that the user edit page works"""
        url: str = reverse('admin:core_user_change', args=[self.user.id])
        res: str = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self) -> None:
        """Test that the create user page works"""
        url: str = reverse('admin:core_user_add')
        res: str = self.client.get(url)

        self.assertEqual(res.status_code, 200)