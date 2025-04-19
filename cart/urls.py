from django.urls import path
from .views import CartListView, AddToCartView, RemoveFromCartView, ClearCartView, SessionCartView

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<int:product_id>', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),

    # Route pour la panier des non-connectés
    path('session-cart/', SessionCartView.as_view(), name='session-cart'),
]
