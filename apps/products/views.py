from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.products.models import Product

def product_list_web(request):
    """
    Vue web pour afficher la page d'accueil avec le catalogue de produits et recherche.
    """
    category_slug = request.GET.get('category')
    q = request.GET.get('q')
    
    products = Product.objects.filter(is_available=True).select_related('category')
    
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'seller':
        products = products.filter(seller=request.user)
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    if q:
        products = products.filter(name__icontains=q)
        
    products = products.order_by('-created_at')[:20]
    
    FAQ_ITEMS = [
        ("Comment passer une commande ?", "Ajoutez votre produit au panier, créez un compte ou connectez-vous, puis finalisez votre achat en quelques clics via notre paiement sécurisé."),
        ("Quels sont les délais de livraison ?", "Nous expédions sous 24–48h ouvrées. La livraison prend en général 3 à 5 jours selon votre localisation."),
        ("Puis-je retourner un produit ?", "Oui, vous disposez de 30 jours après réception pour retourner tout produit non utilisé, dans son emballage d'origine. Le remboursement est effectué sous 5 jours ouvrés."),
    ]

    context = {
        'products': products,
        'selected_category': category_slug,
        'faq_static': FAQ_ITEMS,
        'criteres': [
            'Qualité durable',
            'Utilité réelle',
            'Design soigné',
            'Rapport qualité-prix honnête',
        ],
    }
    return render(request, 'products/product_list.html', context)

def product_detail_web(request, pk):
    """
    Vue web pour afficher les détails d'un produit.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
