from rest_framework.viewsets import ModelViewSet
from apps.categories.models import Category
from api.serializers.category_serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer