# Create your models here.
from django.db import models
from users.models import CustomUser # Import du modele utilisateur

class Category(models.Model):
    """Modele pour classer les produit par categories"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True) # Nom de la categories
    description = models.CharField(max_length=655, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    """Modele representent un produit en vente"""

    id = models.AutoField(primary_key=True)  # Clé primaire auto-incrémentée
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", blank=True, null=True)  # Vendeur (anciennement seller)
    name = models.CharField(max_length=255)  # Nom du produit
    description = models.TextField()  # Description complète
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix
    image = models.ImageField(upload_to='produits/', blank=True, null=True)  # Stocke l'URL de la photo (anciennement image)
    stock_quantity = models.PositiveIntegerField()  # Quantité disponible (anciennement stock)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")  # Catégorie du produit
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"{self.name} - {self.vendor.username}"

class ProductAttribute(models.Model):
    """Modèle pour stocker des atttibuts dynamiques des produits"""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=255) #Ex: "Taille", "Couleur", "Memoire RAM"
    value = models.CharField(max_length=255) #Ex: "Rouge", "128 Go", "L"

    def __str__(self):
        return f"{self.name}: {self.value}"