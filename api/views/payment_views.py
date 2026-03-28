from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.orders.models import Order
from apps.users.permissions import IsCustomer
from core.exceptions.http_exceptions import NotFoundException, PermissionDeniedException
from services.payment_service import process_payment
from api.serializers.payment_serializers import PaymentSerializer


class PaymentView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        order_id = request.data.get('order_id')

        #Vérifier que la commande existe
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFoundException("Commande introuvable")

        #Vérifier que la commande appartient à l'utilisateur connecté
        if order.user != request.user:
            raise PermissionDeniedException()

        payment = process_payment(order_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)