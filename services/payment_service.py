import uuid
from apps.payments.models import Payment
from apps.orders.models import Order
from core.exceptions.business_exceptions import AlreadyPaidException

#Simuler paiement
def process_payment(order_id):
    order = Order.objects.get(id=order_id)

    if order.status == 'paid':
        raise AlreadyPaidException()

    payment,_ = Payment.objects.get_or_create(
        order=order,
        amount=order.total_price
    )

    #simulation de paiement réussi
    payment.status = 'completed'
    payment.transaction_id = str(uuid.uuid4())
    payment.save()

    #update order
    order.status = 'paid'
    order.save()

    return payment