from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from apps.orders.models import Order
from services.payment.payment_service import process_payment

from django.conf import settings

@csrf_exempt
def flutterwave_webhook(request):
    """
    Webhook indépendant gérant les événements système de paiement.
    """
    secret_hash = getattr(settings, 'FLW_WEBHOOK_SECRET', None)
    signature = request.headers.get('verif-hash')
    if secret_hash and signature != secret_hash:
        return JsonResponse({"error": "unauthorized"}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"status": "invalid payload"}, status=400)

    status = payload.get("status")
    tx_ref = payload.get("tx_ref")

    if not tx_ref:
        return JsonResponse({"error": "missing tx_ref"}, status=400)

    if status == "successful":
        try:
            order_id = tx_ref.split("_")[1]
            order = Order.objects.get(id=order_id)

            process_payment(order.id, order.user)

        except Order.DoesNotExist:
            return JsonResponse({"error": "order not found"}, status=400)

    return JsonResponse({"status": "ok"})