from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, User.Roles.CUSTOMER)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo', role=User.Roles.ADMIN)
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class UserModelIntegrationTests(TestCase):
    def test_manager_role_assigns_staff_status(self):
        user = User.objects.create_user(email='manager@test.com', password='foo', role=User.Roles.MANAGER)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name='Managers').exists())

    def test_seller_role_assigns_staff_status(self):
        user = User.objects.create_user(email='seller@test.com', password='foo', role=User.Roles.SELLER)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name='Sellers').exists())

    def test_customer_role_removes_staff_status(self):
        user = User.objects.create_user(email='customer@test.com', password='foo', role=User.Roles.MANAGER)
        self.assertTrue(user.is_staff)
        
        user.role = User.Roles.CUSTOMER
        user.save()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.groups.filter(name='Managers').exists())
