from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.cart_service import add_to_cart, remove_from_cart
from apps.cart.models import Cart
from core.exceptions.base import BaseAPIException

@login_required(login_url='/users/login/')
def cart_detail_web(request):
    """Affiche le contenu du panier et le prix total."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    
    # Calcul du total et annotation line_total sur chaque item
    for item in items:
        item.line_total = item.product.price * item.quantity
    total = sum(item.line_total for item in items)
    
    context = {
        'items': items,
        'total': total
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required(login_url='/users/login/')
def add_to_cart_web(request):
    """Ajoute une quantité spécifique d'un produit au panier via POST."""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            add_to_cart(request.user, product_id, quantity)
            messages.success(request, "Produit ajouté au panier.")
        except BaseAPIException as e:
            messages.error(request, str(e.default_detail))
        except Exception as e:
            messages.error(request, "Erreur lors de l'ajout au panier.")
            
    return redirect('cart:detail')

@login_required(login_url='/users/login/')
def remove_from_cart_web(request, product_id):
    """Retire un produit spécifique du panier utilisateur."""
    if request.method == 'POST':
        try:
            remove_from_cart(request.user, product_id)
            messages.success(request, "Produit retiré du panier.")
        except Exception:
            messages.error(request, "Impossible de retirer le produit.")
    return redirect('cart:detail')
