# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Vue pour lister et creer les produits 
class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET : Recuperer la liste des produits.
    POST : Ajouter un produit (reserver aux vendeurs).

    Vue permettant :
    - De récupérer la liste des produits avec des filtres avancés
    - D'ajouter un produit (réservé aux vendeurs)
    """

    queryset = Product.objects.all() # Recupere tous les produits ( le filtrage se fait par via l'URL)
    serializer_class = ProductSerializer # Utilise le serialiseur pour traiter les donnees
    parser_classes = (MultiPartParser, FormParser) # Permet de gérer les fichiers
    # Ajouter des filtres avancés
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtre disponible dans l'API (ex: ?category=1)
    filterset_fields =['category', 'vendor', 'price', 'stock_quantity']

    # Recherche possible sur le nom et description du produit (ex: search=iphone)
    search_fields = ['name', 'description']

    # Peermet de trier les resultats par exemple (ordering=price ou ordering=-price)
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        """
        Surcharge de la methode create pour associer le produit a son createur.
        Lorsqu'un utilisateur  (vendeur) ajoute un produit, il est automatiquement associer a lui.
        """
        serializer.save(seller=self.request.user) # Associe le produit au vendeur qui l'a cree

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Cette vue permet :
    -GET : Voir les details d'un produit (uniquement si c'est le proprietaire).
    -PUT/PATCH : Modifier un produit (uniquement si c'est le proprietaire).
    -DELETE : Suprimer un produit (uniquememt si c'est le proprietaire)
    """

    queryset = Product.objects.all() #Recupere tout les produits (via l'URL)
    serializer_class = ProductSerializer # Utiliser le serialiseur pour traiter les donnees

    def get_permissions(self):
        """
        Definit les permissions selon les types de requetes :
        - Seuls les utilisateurs authentifiers peuvent modifier ou suprimer un produit.
        - Tout le monde peut voir les produits (GET n'a pas besoin de permissions speciales).
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']: # Si la requete est une modification ou une une supression
            return [permissions.IsAuthenticated()] # Seuls les utilisateurs connectes peuvent modifier/supprimer
        return [] # GET ne necessite pas d'authentification
    
