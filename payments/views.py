from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings



class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)

    def create(self, request, *args, **kwargs):
        # Implémentez la logique de paiement avec Stripe ici
        pass