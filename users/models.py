from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_seller="0", profile_picture=None):
        if not email:
            raise ValueError("L'email est obligatoire")
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_seller=is_seller,
            profile_picture=profile_picture
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            is_seller="2"  # "2" = Administrateur
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé"""

    SELLER_CHOICES = [
        ("0", "Client"),
        ("1", "Vendeur"),
        ("2", "Administrateur"),
    ]

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    is_seller = models.CharField(max_length=1, choices=SELLER_CHOICES, default="0")
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
