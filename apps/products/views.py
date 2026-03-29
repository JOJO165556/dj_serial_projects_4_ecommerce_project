from django.shortcuts import render, get_object_or_404
from apps.products.models import Product

def product_list_web(request):
    """
    Vue web pour afficher la page d'accueil avec le catalogue de produits.
    """
    category_slug = request.GET.get('category')
    products = Product.objects.filter(is_available=True).select_related('category')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    products = products.order_by('-created_at')[:20]
    
    context = {
        'products': products,
        'selected_category': category_slug
    }
    return render(request, 'products/product_list.html', context)

def product_detail_web(request, pk):
    """
    Vue web pour afficher les détails d'un produit.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
