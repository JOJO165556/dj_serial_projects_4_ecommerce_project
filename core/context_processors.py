from apps.categories.models import Category

def category_processor(request):
    """
    Rend les catégories disponibles globablement dans tous les templates
    (pour le menu déroulant par exemple).
    On ne prend que les catégories parentes actives.
    """
    categories_menu = Category.objects.filter(is_active=True, parent__isnull=True).order_by('name')
    return {
        'categories_menu': categories_menu
    }
