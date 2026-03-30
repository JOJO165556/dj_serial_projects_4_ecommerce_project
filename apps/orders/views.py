from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.models import Cart
from services.order_service import create_order
from services.payment.flutterwave import create_flutterwave_payment, verify_flutterwave_payment
from services.payment.payment_service import process_payment
from .forms import OrderCheckoutForm
from apps.orders.models import Order
from core.exceptions.base import BaseAPIException
from django.conf import settings

@login_required(login_url='/users/login/')
def order_history_web(request):
    """Affiche l'historique des commandes de l'utilisateur."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

@login_required(login_url='/users/login/')
def checkout_web(request):
    """Gère l'affichage du formulaire de commande et l'initiation du paiement."""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.select_related('product').all()
        if not items:
            messages.warning(request, "Votre panier est vide.")
            return redirect('cart:detail')
    except Cart.DoesNotExist:
        return redirect('products:home')

    total = sum(item.product.price * item.quantity for item in items)
    
    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data.get('shipping_address')
            try:
                order = create_order(request.user, shipping_address=shipping_address)
                # Sauvegarde du montant total sur la commande
                order.total_price = total
                order.save(update_fields=['total_price'])
                # Appel API Flutterwave
                flw_resp = create_flutterwave_payment(order, request.user, request=request)
                if flw_resp.get('status') == 'success' and 'data' in flw_resp and 'link' in flw_resp['data']:
                    messages.info(request, "Redirection vers le portail de paiement sécurisé...")
                    return redirect(flw_resp['data']['link'])
                else:
                    err = flw_resp.get('message', 'Erreur API Flutterwave.')
                    messages.error(request, f"Paiement impossible: {err}")
            except BaseAPIException as e:
                messages.error(request, str(e.default_detail))
                
    else:
        form = OrderCheckoutForm()
        
    context = {
        'items': items,
        'total': total,
        'form': form
    }
    return render(request, 'orders/checkout.html', context)

@login_required(login_url='/users/login/')
def order_success_web(request):
    """
    Page de confirmation juste après le paiement Flutterwave sur l'URL de redirect.
    """
    tx_ref = request.GET.get('tx_ref', '')
    transaction_id = request.GET.get('transaction_id', '')
    status = request.GET.get('status', '')
    
    order_id = False
    if tx_ref.startswith('order_'):
        parts = tx_ref.split('_')
        if len(parts) >= 2:
            order_id = parts[1]
            try:
                order = Order.objects.get(id=order_id)
                
                # FALLBACK LOCALHOST: 
                # Le webhook FLW ne peut pas atteindre une url localhost.
                # Donc on vérifie directement la transaction si on est redirigé avec "successful"
                if status == 'successful' and transaction_id and order.status == 'pending':
                    verify_resp = verify_flutterwave_payment(transaction_id)
                    if verify_resp.get('status') == 'success' and verify_resp.get('data', {}).get('status') == 'successful':
                        # Traiter le paiement
                        process_payment(order.id, request.user)
                        
            except Order.DoesNotExist:
                pass
            
    context = {
        'order_id': order_id,
        'status': status
    }
    return render(request, 'orders/success.html', context)
