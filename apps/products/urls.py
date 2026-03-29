from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_web, name='home'),
    path('<int:pk>/', views.product_detail_web, name='detail'),
]
