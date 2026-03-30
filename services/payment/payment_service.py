from django.db import transaction

from apps.orders.models import Order
from apps.payments.models import Payment
from core.exceptions.business_exceptions import OutOfStockException, AlreadyPaidException
from core.exceptions.http_exceptions import PermissionDeniedException, NotFoundException

@transaction.atomic
def process_payment(order_id, user):
    try:
        order = Order.objects.select_related('user').prefetch_related('items__product').get(id=order_id)
    except Order.DoesNotExist:
        raise NotFoundException("Order not found")

    if order.user != user:
        raise PermissionDeniedException()

    if order.status == 'paid':
        raise AlreadyPaidException()

    for item in order.items.all():
        product = item.product

        if product.stock < item.quantity:
            raise OutOfStockException()

        product.stock -= item.quantity
        product.save()

    payment, _ = Payment.objects.get_or_create(
        order=order,
        amount=order.total_price
    )
    payment.status = 'completed'
    payment.save(update_fields=['status'])

    order.status = 'paid'
    order.save(update_fields=['status'])

    return payment