from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Vendor, Shop
from .serializers import (
    VendorSerializer, 
    VendorDetailSerializer,
    VendorCreateSerializer,
    ShopSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVendorOrReadOnly, IsAdminOrReadOnly

User = get_user_model()

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.filter(is_approved=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendorCreateSerializer
        return VendorSerializer

class VendorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailSerializer
    permission_classes = [IsAuthenticated, IsVendorOrReadOnly]

    def perform_update(self, serializer):
        vendor = self.get_object()
        user = vendor.user
        
        # Mise à jour des champs de base
        vendor = serializer.save()
        
        # Mise à jour de la boutique si les données sont fournies
        shop_data = self.request.data.get('shop', None)
        if shop_data and hasattr(vendor, 'shop'):
            shop = vendor.shop
            shop_serializer = ShopSerializer(shop, data=shop_data, partial=True)
            if shop_serializer.is_valid():
                shop_serializer.save()

class ShopListAPIView(generics.ListAPIView):
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

class ShopDetailAPIView(generics.RetrieveAPIView):
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'