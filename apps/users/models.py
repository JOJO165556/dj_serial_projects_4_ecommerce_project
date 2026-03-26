from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        SELLER = "seller", "Seller"
        CUSTOMER = "customer", "Customer"
        
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CUSTOMER
    )