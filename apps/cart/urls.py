from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_web, name='detail'),
    path('add/', views.add_to_cart_web, name='add'),
    path('remove/<int:product_id>/', views.remove_from_cart_web, name='remove'),
]
