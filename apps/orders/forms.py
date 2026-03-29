from django import forms
from apps.orders.models import Order

class OrderCheckoutForm(forms.ModelForm):
    """Formulaire de sélection de l'adresse de livraison lors du checkout."""
    class Meta:
        model = Order
        fields = ('shipping_address',)
        labels = {
            'shipping_address': 'Adresse de livraison complète'
        }
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'De quelle façon souhaitez-vous être livré ? (Ex: 12 Rue de la Paix, 75000 Paris, France)'
            })
        }
