from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem

#Créer commande depuis panier
def create_order(user):
    cart = Cart.objects.create(user=user)
    items = cart.items.all()

    if not items:
        return None

    order = Order.objects.create(user=user)
    total = 0

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        total += item.product.price * item.quantity

    order.total_price = total
    order.save()

    cart.items.all().delete()

    return order