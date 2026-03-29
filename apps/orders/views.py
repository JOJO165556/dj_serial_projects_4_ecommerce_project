from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.models import Cart
from services.order_service import create_order
from services.payment.flutterwave import create_flutterwave_payment
from .forms import OrderCheckoutForm
from core.exceptions.base import BaseAPIException
from django.conf import settings
from django.conf import settings

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
                # Appel API Flutterwave
                flw_resp = create_flutterwave_payment(order, request.user)
                if flw_resp.get('status') == 'success' and 'data' in flw_resp and 'link' in flw_resp['data']:
                    messages.info(request, "Redirection vers le portail de paiement sécurisé...")
                    return redirect(flw_resp['data']['link'])
                else:
                    messages.error(request, "Erreur avec l'API Flutterwave. Veuillez réessayer.")
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
            
    context = {
        'order_id': order_id,
        'status': status
    }
    return render(request, 'orders/success.html', context)
