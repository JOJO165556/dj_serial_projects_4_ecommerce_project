from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsCustomer
from services.cart_service import add_to_cart, remove_from_cart, clear_cart

from apps.cart.models import Cart
from api.serializers.cart_serializers import CartSerializer


# Voir panier
class CartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# Ajouter produit
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        item = add_to_cart(request.user, product_id, quantity)

        return Response({
            "message": "Produit ajouté au panier",
            "item_id": item.id
        }, status=status.HTTP_201_CREATED)


# Supprimer produit
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        product_id = request.data.get('product_id')
        remove_from_cart(request.user, product_id)

        return Response({"message": "Produit supprimé"})


# Vider panier
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        clear_cart(request.user)
        return Response({"message": "Panier vidé"})
