from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart
from products.models import Product
from .serializers import CartSerializer

# Create your views here.
#-------------------Cart en Base de Données-------------------------------------

# Affichage du panier
class CartListView(generics.ListAPIView):
    """Voir le contenu du panier"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
        
# Ajout au panier
class AddToCartView(APIView):
    """Ajouter un produit au panier"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantite += quantity
            cart_item.save()
            
        return Response({"message": "Produit ajouté au panier avec succès !"})
    
# Suppression d'un élément du panier
class RemoveFromCartView(APIView):
    """Supprimer un produit du panier"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        Cart.objects.filter(user=request.user, product_id=product_id).delete()
        return Response({"message": "produit supprimer du panier"})

# Supprimer tout les éléments du panier
class ClearCartView(APIView):
    """Vider completement le panier"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Panier vider avec succès"})

    
#-------------------Gestion des sessions pour les Non-Connectés------------------------------------

class SessionCartView(APIView):
    """Gestion des sessions pour les utilisateurs non connectés"""

    def get(self, request):
        """Voir le contenu du panier(Session)"""
        cart = request.session.get('cart', {})
        return Response(cart)

    def post (self, request):
        """Ajouter un produit au panier (Session)"""
        product_id = str(request.data.get("product_id"))
        quantity = int(request.data.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        # Récuperer ou créer le panier en session
        cart = request.session.get('cart', {})

        # Ajouter/Modifié le produit dans le panier
        if product_id in cart:
            cart[product_id]["quantity"] += quantity
        else:
            cart[product_id] = {
                "name": product.name,
                "price": str(product.price),
                "quantite": quantity
            }

            # Sauvegarder la session
            request.session["cart"] = cart
            request.session.modified = True

            return Response({"message": "Produit ajouté au panier (Mode Session) !"})
        
    def delete(self, request):
        """Vider complètememt le panier"""
        request.session["cart"] = {}
        request.session.modified =True
        return Response({"message": "Panier vidé avec succès (Mode Session)"})