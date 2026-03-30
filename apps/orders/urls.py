from django.urls import path

from . import views
from webhooks.flutterwave import flutterwave_webhook

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_web, name='checkout'),
    path('history/', views.order_history_web, name='history'),
    path('webhook/flutterwave/', flutterwave_webhook, name='webhook'),
]
