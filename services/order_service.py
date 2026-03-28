from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from core.exceptions.business_exceptions import EmptyCartException

#Créer commande depuis panier
def create_order(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    items = cart.items.select_related('product').all()

    if not items:
        raise EmptyCartException()

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

    # Prefetch pour éviter N+1 à la sérialisation
    order = Order.objects.prefetch_related('items__product').get(id=order.id)

    return order