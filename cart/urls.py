from django.urls import path
from . import views  # Assure-toi que tu as créé des vues pour gérer ces routes

# Définition des URL pour l'application 'cart'
urlpatterns = [
    # Exemple : une vue qui affiche les produits dans le panier
    path('', views.cart_view, name='cart_view'),
    # Si tu as une vue pour ajouter un article au panier :
    path('add/', views.add_to_cart, name='add_to_cart'),
    # Et une pour supprimer un article du panier :
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
]
