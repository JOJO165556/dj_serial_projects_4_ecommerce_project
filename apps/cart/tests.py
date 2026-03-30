from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.cart.models import Cart, CartItem
from apps.categories.models import Category
from services.cart_service import add_to_cart, remove_from_cart, clear_cart

User = get_user_model()

class CartServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='customer@test.com', password='foo')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product1 = Product.objects.create(
            seller=self.user,
            category=self.category,
            name='Product 1',
            slug='product-1',
            price=15.00,
            stock=10
        )
        self.product2 = Product.objects.create(
            seller=self.user,
            category=self.category,
            name='Product 2',
            slug='product-2',
            price=20.00,
            stock=5
        )

    def test_add_to_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        add_to_cart(self.user, self.product1.id, 2)
        
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product.id, self.product1.id)

    def test_remove_from_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        add_to_cart(self.user, self.product1.id, 1)
        remove_from_cart(self.user, self.product1.id)
        
        self.assertEqual(cart.items.count(), 0)

    def test_clear_cart(self):
        add_to_cart(self.user, self.product1.id, 1)
        add_to_cart(self.user, self.product2.id, 1)
        clear_cart(self.user)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)
