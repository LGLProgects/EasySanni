from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupportTicketViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'support-tickets', SupportTicketViewSet, basename='support-ticket')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]