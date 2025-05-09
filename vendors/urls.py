from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorDetailAPIView,
    ShopListAPIView,
    ShopDetailAPIView
)

urlpatterns = [
    path('', VendorListCreateAPIView.as_view(), name='vendor-list'),
    path('<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('shops/', ShopListAPIView.as_view(), name='shop-list'),
    path('shops/<slug:slug>/', ShopDetailAPIView.as_view(), name='shop-detail'),
]