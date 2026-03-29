from django.contrib import admin
from django.urls import path, include
from apps.orders import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.products.urls', namespace='products')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('payment/success/', views.order_success_web, name='payment_success'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )