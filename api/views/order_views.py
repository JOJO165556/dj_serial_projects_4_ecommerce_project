from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.orders.models import Order
from apps.users.permissions import IsCustomer
from core.exceptions.http_exceptions import NotFoundException
from services.order_service import create_order
from api.serializers.order_serializers import OrderSerializer


# Créer commande
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        order = create_order(request.user)

        if not order:
            return Response(
                {"error": "Panier vide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Voir ses commandes
class UserOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related('items__product')
            .order_by('-created_at')
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# Détail d'une commande
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, pk):
        try:
            order = (
                Order.objects
                .prefetch_related('items__product')
                .get(id=pk, user=request.user)
            )
        except Order.DoesNotExist:
            raise NotFoundException("Order not found")
        serializer = OrderSerializer(order)
        return Response(serializer.data)