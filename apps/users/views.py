from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_web(request):
    """Gère l'inscription d'un nouveau client via le web."""
    if request.user.is_authenticated:
        return redirect('products:home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            name = user.email.split('@')[0].capitalize()
            messages.success(request, f"Bienvenue {name} ! Votre compte a été créé avec succès.")
            return redirect('products:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_web(request):
    """Authentifie et connecte un utilisateur via email et mot de passe."""
    if request.user.is_authenticated:
        return redirect('products:home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            name = user.email.split('@')[0].capitalize()
            messages.success(request, f"Heureux de vous revoir, {name} !")
            return redirect('products:home')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

def logout_web(request):
    """Déconnecte l'utilisateur courant et redirige vers l'accueil."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('products:home')
