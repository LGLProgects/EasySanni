from rest_framework import serializers
from .models import SupportTicket, Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'read', 'attachments']
        read_only_fields = ['id', 'sender', 'timestamp']

class SupportTicketSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['id', 'ticket_type', 'status', 'subject', 'created_at',
                  'updated_at', 'from_user', 'to_user', 'related_order',
                  'related_product', 'messages']
        read_only_fields = ['id', 'created_at', 'updated_at']
