from rest_framework import serializers 
from .models import Product   

class ProductSerializer(serializers.ModelSerializer):
    """
        Convertit le model Product en JSON
        Serializeur pour les produits avec gestion des images
    """
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'description', 'price', 'image', 'stock_quantity', 'category', 'created_at']