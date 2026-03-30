import requests
from django.conf import settings

def create_flutterwave_payment(order, user, request=None):
    """Génère une session de paiement Flutterwave et retourne le lien de redirection."""
    url = "https://api.flutterwave.com/v3/payments"

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    if request:
        from django.urls import reverse
        redirect_url = request.build_absolute_uri(reverse('payment_success'))
    else:
        redirect_url = getattr(settings, 'FLW_REDIRECT_URL', "http://127.0.0.1:8000/payment/success/")

    data = {
        "tx_ref": f"order_{order.id}_{user.id}",
        "amount": float(order.total_price),
        "currency": "XOF",
        "redirect_url": redirect_url,
        "customer": {
            "email": user.email,
            "name": user.username
        },
        "customizations": {
            "title": "Order Payment",
            "description": f"Payment for order {order.id}"
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def verify_flutterwave_payment(transaction_id):
    """Vérifie le statut d'une transaction directement auprès de l'API Flutterwave."""
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()