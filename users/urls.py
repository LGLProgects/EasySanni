from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    UserRegisterView,
    SellerRegisterView,
    UserProfileView,
    UserListView,
    UpgradeToSellerView
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('upgrade/seller/', UpgradeToSellerView.as_view(), name='upgrade-seller'),
]