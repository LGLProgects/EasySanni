from django.db import models
from users.models import CustomUser
from products.models import Product

# Create your models here.
class Cart(models.Model):
    """Panier d'achat lié à un utilisateur"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} x {self.produit.name} dans le panier de {self.user.username}"
    
class CartItem(models.Model):
    """Produit dans le panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product') # pour éviter les doublons de produits

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"