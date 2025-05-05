from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SupportTicket(models.Model):
    TICKET_TYPES = [
        ('CLIENT_ADMIN', 'Client vers Administration'),
        ('VENDOR_ADMIN', 'Vendeur vers Administration'),
        ('ADMIN_CLIENT', 'Administration vers Client'),
        ('ADMIN_VENDOR', 'Administration vers Vendeur'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Ouvert'),
        ('IN_PROGRESS', 'En cours'),
        ('RESOLVED', 'Résolu'),
        ('CLOSED', 'Fermé'),
    ]

    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    from_user = models.ForeignKey(User, related_name='sent_tickets', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_tickets', on_delete=models.CASCADE)
    related_order = models.ForeignKey('orders.Order', null=True, blank=True, on_delete=models.SET_NULL)
    related_product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL)

class Message(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    attachments = models.FileField(upload_to='message_attachments/', null=True, blank=True)