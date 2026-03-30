from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.categories.models import Category

User = get_user_model()

class ProductModelTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            email='seller_test@test.com', 
            password='foo', 
            role=User.Roles.SELLER
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=19.99,
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.is_available)

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), self.product.name)
