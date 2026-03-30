from apps.categories.models import Category
from apps.cart.models import Cart

def category_processor(request):
    """
    Rend les catégories disponibles globablement dans tous les templates
    (pour le menu déroulant par exemple).
    On ne prend que les catégories parentes actives.
    """
    categories_menu = Category.objects.filter(is_active=True, parent__isnull=True).order_by('name')
    
    # Récupérer le nombre total d'articles dans le panier (uniquement si utilisateur authentifié)
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            pass

    return {
        'categories_menu': categories_menu,
        'cart_count': cart_count,
    }
