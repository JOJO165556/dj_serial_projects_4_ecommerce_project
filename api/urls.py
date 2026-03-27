from django.urls import path, include
from api.routers import router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views.auth_views import RegisterView, LogoutView
from api.views.cart_views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    ClearCartView
)

from api.views.order_views import (
    CreateOrderView,
    UserOrderView,
    OrderDetailView
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
]

urlpatterns += [
    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/remove/', RemoveFromCartView.as_view()),
    path('cart/clear/', ClearCartView.as_view()),
]

urlpatterns += [
    path('orders/create/', CreateOrderView.as_view()),
    path('orders/', UserOrderView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]