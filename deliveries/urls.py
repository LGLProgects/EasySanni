from django.urls import path
from .views import (
    DeliveryListView,
    DeliveryDetailView,
    DeliveryAssignView,
    DeliveryUpdateView,
    ReturnCreateView,
    ReturnDetailView
)

urlpatterns = [
    path('', DeliveryListView.as_view(), name='delivery-list'),
    path('<int:pk>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('<int:pk>/assign/', DeliveryAssignView.as_view(), name='delivery-assign'),
    path('<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery-update'),
    path('returns/', ReturnCreateView.as_view(), name='return-create'),
    path('returns/<int:pk>/', ReturnDetailView.as_view(), name='return-detail'),
]
