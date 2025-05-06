from django.db import models

class Delivery(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'en attente'),
        ('attribue', 'attribué'),
        ('en_transi', 'en transit'),
        ('livres', 'livrés'),
    )

    order_id = models.CharField(max_length=100, unique=True)
    seller_id = models.CharField(max_length=100)
    delivery_man_id = models.CharField(max_length=100, blank=True, null=True)
    customer_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.order_id} - {self.status}"


class DeliveryStep(models.Model):
    STEP_CHOICES = (
        ('transfert_vendeur', 'transfert vendeur'),
        ('enlevement_par_un_livreur', 'enlèvement par un livreur'),
        ('client_recu', 'client reçu'),
    )

    delivery = models.ForeignKey(Delivery, related_name='steps', on_delete=models.CASCADE)
    step = models.CharField(max_length=50, choices=STEP_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.step} for {self.delivery.order_id}"


class Return(models.Model):
    STATUS_CHOICES = (
        ('demandee', 'demandée'),
        ('approuvee', 'approuvé'),
        ('rejetee', 'rejeté'),
        ('achevee', 'achevé'),
    )

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='demandee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return for {self.delivery.order_id} - {self.status}"
