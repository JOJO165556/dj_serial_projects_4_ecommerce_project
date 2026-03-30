from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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

    def save(self, *args, **kwargs):
        # Sécurité : définir is_staff et is_superuser automatiquement selon le rôle
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role in [self.Roles.MANAGER, self.Roles.SELLER]:
            self.is_staff = True
            self.is_superuser = False
        else:  # CUSTOMER
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

        # Assigner au groupe correspondant après la sauvegarde (id existant requis)
        from django.contrib.auth.models import Group
        if self.role == self.Roles.MANAGER:
            group, _ = Group.objects.get_or_create(name='Managers')
            self.groups.set([group])
        elif self.role == self.Roles.SELLER:
            group, _ = Group.objects.get_or_create(name='Sellers')
            self.groups.set([group])
        elif self.role == self.Roles.CUSTOMER:
            self.groups.clear()

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name ='profile'
    )

    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    business_name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return f"Profile of {self.user}"