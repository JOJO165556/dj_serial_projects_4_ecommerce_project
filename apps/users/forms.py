from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription pour l'interface web."""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Force le rôle par défaut "Client" pour les inscriptions web
        user.role = User.Roles.CUSTOMER
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire de connexion web basé sur l'email."""
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
