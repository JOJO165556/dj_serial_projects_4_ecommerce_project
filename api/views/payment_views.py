from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order
from core.exceptions.business_exceptions import AlreadyPaidException
from core.exceptions.http_exceptions import NotFoundException
from services.payment.flutterwave import create_flutterwave_payment


class InitPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            raise NotFoundException("Order not found")

        if order.status == "paid":
            raise AlreadyPaidException()

        response = create_flutterwave_payment(order, request.user)

        return Response(response)