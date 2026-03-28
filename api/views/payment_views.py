from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from services.payment_service import process_payment
from api.serializers.payment_serializers import PaymentSerializer

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        payment = process_payment(order_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)