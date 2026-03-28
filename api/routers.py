from rest_framework.routers import DefaultRouter
from api.views.product_viewsets import ProductViewSet
from api.views.category_viewsets import CategoryViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = router.urls