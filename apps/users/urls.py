from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_web, name='login'),
    path('register/', views.register_web, name='register'),
    path('logout/', views.logout_web, name='logout'),
]
