from django.urls import path
from .views import (
    CartListView,
    AddToCartView,
    UpdateCartItemView,
    RemoveFromCartView,
    ClearCartView,
    SessionCartView,
    FusionnerPanierView,
    ProductReviewListView,
    AddReviewView,
    UpdateReviewView,
    DeleteReviewView
)


urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/<int:id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/<int:id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),

    path('reviews/<int:productId>/', ProductReviewListView.as_view(), name='product-reviews'),
    path('reviews/add/', AddReviewView.as_view(), name='add-review'),
    path('reviews/update/<int:id>/', UpdateReviewView.as_view(), name='update-review'),
    path('reviews/delete/<int:id>/', DeleteReviewView.as_view(), name='delete-review'),
    path('session-cart/', SessionCartView.as_view(), name='session-cart'),
    path('merge-cart/', FusionnerPanierView.as_view(), name='merge-cart'),


]
