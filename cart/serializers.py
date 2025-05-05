from rest_framework import serializers 
from .models import Cart   

class CartSerializer(serializers.ModelSerializer):
    """
        Convertit le model Product en JSON
        Serializeur pour les produits avec gestion des images
    """
    class Meta:
        model = Cart
        fields = ['user', 'produit', 'quantite', 'added_at']