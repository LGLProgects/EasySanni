# admin_panel/views.py

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from .models import Product, Notification
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Vue pour lister et creer les produits
class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET : Recuperer la liste des produits.
    POST : Ajouter un produit (réservé aux vendeurs).

    Vue permettant :
    - De récupérer la liste des produits avec des filtres avancés
    - D'ajouter un produit (réservé aux vendeurs)
    """

    queryset = Product.objects.all()  # Récupère tous les produits (le filtrage se fait via l'URL)
    serializer_class = ProductSerializer  # Utilise le serializer pour traiter les données
    parser_classes = (MultiPartParser, FormParser)  # Permet de gérer les fichiers

    # Ajouter des filtres avancés
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtre disponible dans l'API (ex: ?category=1)
    filterset_fields = ['category', 'vendor', 'price', 'stock_quantity']

    # Recherche possible sur le nom et description du produit (ex: search=iphone)
    search_fields = ['name', 'description']

    # Permet de trier les résultats par exemple (ordering=price ou ordering=-price)
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        """
        Surcharge de la méthode create pour associer le produit à son créateur.
        Lorsqu'un utilisateur (vendeur) ajoute un produit, il est automatiquement associé à lui.
        """
        serializer.save(seller=self.request.user)  # Associe le produit au vendeur qui l'a créé

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Cette vue permet :
    - GET : Voir les détails d'un produit (uniquement si c'est le propriétaire).
    - PUT/PATCH : Modifier un produit (uniquement si c'est le propriétaire).
    - DELETE : Supprimer un produit (uniquement si c'est le propriétaire).
    """

    queryset = Product.objects.all()  # Récupère tous les produits (via l'URL)
    serializer_class = ProductSerializer  # Utilise le serializer pour traiter les données

    def get_permissions(self):
        """
        Définit les permissions selon les types de requêtes :
        - Seuls les utilisateurs authentifiés peuvent modifier ou supprimer un produit.
        - Tout le monde peut voir les produits (GET n'a pas besoin de permissions spéciales).
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:  # Si la requête est une modification ou une suppression
            return [permissions.IsAuthenticated()]  # Seuls les utilisateurs connectés peuvent modifier/supprimer
        return []  # GET ne nécessite pas d'authentification

# Vue pour afficher les notifications
def notifications_view(request):
    """
    Affiche une liste de notifications.
    """
    notifications = Notification.objects.all()  # Récupère toutes les notifications
    return render(request, 'notifications/list.html', {'notifications': notifications})
