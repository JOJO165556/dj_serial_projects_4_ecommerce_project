from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription pour l'interface web."""
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'vous@exemple.com', 'autocomplete': 'email'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels français
        self.fields['password1'].label = "Mot de passe"
        self.fields['password1'].widget.attrs.update({'placeholder': '••••••••'})
        self.fields['password1'].help_text = "8 caractères minimum. Mélangez lettres et chiffres."
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['password2'].widget.attrs.update({'placeholder': '••••••••'})
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.CUSTOMER
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire de connexion web basé sur l'email."""
    username = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'vous@exemple.com', 'autocomplete': 'email'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = "Mot de passe"
        self.fields['password'].widget.attrs.update({'placeholder': '••••••••'})
