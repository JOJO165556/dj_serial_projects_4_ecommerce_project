import requests
from django.conf import settings

def create_flutterwave_payment(order, user):
    """Génère une session de paiement Flutterwave et retourne le lien de redirection."""
    url = "https://api.flutterwave.com/v3/payments"

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "tx_ref": f"order_{order.id}_{user.id}",
        "amount": float(order.total_price),
        "currency": "XOF",
        "redirect_url": settings.FLW_REDIRECT_URL,
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