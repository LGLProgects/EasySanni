# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Model pour l'utilisateur
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  
    
    def __str__(self):
        return self.email
