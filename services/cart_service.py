from apps.cart.models import Cart, CartItem
from apps.products.models import Product

#Ajouter au panier
def add_to_cart(user, product_id, quantity=1):
    cart,_ = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        item.quantity = quantity # initialisation
    else:
        item.quantity += quantity # addition

    item.save()
    return item

#Retirer du panier
def remove_from_cart(user, product_id):
    cart = Cart.objects.get(user=user)

    CartItem.objects.filter(
        cart=cart,
        product=product_id
    ).delete()

#Vider panier
def clear_cart(user):
    cart = Cart.objects.get(user=user)
    cart.items.all().delete()