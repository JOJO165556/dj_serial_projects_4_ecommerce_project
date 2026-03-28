from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.models import Product
from api.serializers.product_serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter

    #Recherche
    search_fields = ["name", "description"]

    #Tri
    ordering_fields = ['price', 'created_at', 'stock']
    ordering = ('-created_at',)