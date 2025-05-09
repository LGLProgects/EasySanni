from django.urls import path

from admin_panel import views
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('notifications/', views.notifications_view, name='notifications'),
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-list-create'),
]
