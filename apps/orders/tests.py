from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.categories.models import Category
from apps.orders.models import Order
from apps.payments.models import Payment
from services.cart_service import add_to_cart
from services.order_service import create_order
from services.payment.payment_service import process_payment
import decimal

User = get_user_model()

class OrderAndPaymentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='buyer@test.com', password='foo')
        self.seller = User.objects.create_user(email='seller@test.com', password='foo')
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Watch',
            slug='watch',
            price=150.00,
            stock=10
        )
        add_to_cart(self.user, self.product.id, 2)
        
    def test_create_order_from_cart(self):
        order = create_order(self.user, "123 Test St, Test City, +123456789")
        
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_price, decimal.Decimal('300.00'))

    def test_process_payment_updates_stock_and_status(self):
        order = create_order(self.user, "123 Test St, Test City, +123456789")
        
        # Le paiement via webhook/redirection finalise la commande
        payment = process_payment(order.id, self.user)
        
        order.refresh_from_db()
        self.product.refresh_from_db()
        
        self.assertEqual(payment.status, 'completed')
        self.assertEqual(order.status, 'paid')
        self.assertEqual(self.product.stock, 8) # 10 stock initial - 2 achetés
