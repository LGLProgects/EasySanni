from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import SupportTicket, Message
from .serializers import SupportTicketSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return SupportTicket.objects.filter(
                Q(to_user=user) | Q(from_user=user)
            )
        else:
            return SupportTicket.objects.filter(from_user=user)

    def perform_create(self, serializer):
        user = self.request.user
        ticket_type = serializer.validated_data.get('ticket_type')
        
        if user.role == 'CLIENT':
            if ticket_type != 'CLIENT_ADMIN':
                raise serializers.ValidationError("Les clients ne peuvent créer que des tickets CLIENT_ADMIN")
            admin = User.objects.filter(role='ADMIN').first()
            serializer.save(from_user=user, to_user=admin)
        
        elif user.role == 'VENDOR':
            if ticket_type != 'VENDOR_ADMIN':
                raise serializers.ValidationError("Les vendeurs ne peuvent créer que des tickets VENDOR_ADMIN")
            admin = User.objects.filter(role='ADMIN').first()
            serializer.save(from_user=user, to_user=admin)
        
        else:  # ADMIN
            ticket_type = serializer.validated_data.get('ticket_type')
            if ticket_type not in ['ADMIN_CLIENT', 'ADMIN_VENDOR']:
                raise serializers.ValidationError("Type de ticket invalide pour l'admin")
            serializer.save(from_user=user)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        ticket = self.get_object()
        user = request.user
        
        # Vérification des permissions
        if user not in [ticket.from_user, ticket.to_user]:
            return Response(
                {"detail": "Vous n'avez pas accès à ce ticket."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, sender=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        user = request.user
        
        if user.role != 'ADMIN':
            return Response(
                {"detail": "Seul l'admin peut modifier le statut."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(SupportTicket.STATUS_CHOICES).keys():
            return Response(
                {"detail": "Statut invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = new_status
        ticket.save()
        return Response(SupportTicketSerializer(ticket).data)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(ticket__from_user=user) | Q(ticket__to_user=user))
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if message.ticket.to_user != request.user:
            return Response(
                {"detail": "Vous ne pouvez marquer comme lu que les messages qui vous sont destinés."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.read = True
        message.save()
        return Response(MessageSerializer(message).data)