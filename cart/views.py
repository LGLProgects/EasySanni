from django.shortcuts import render

# Vue pour afficher le panier
def cart_view(request):
    return render(request, 'cart/cart_view.html')  # Assure-toi d'avoir un template correspondant

# Vue pour ajouter un produit au panier
def add_to_cart(request):
    # Logique pour ajouter un article au panier
    return render(request, 'cart/cart_view.html')

# Vue pour supprimer un produit du panier
def remove_from_cart(request):
    # Logique pour supprimer un article du panier
    return render(request, 'cart/cart_view.html')
