from rest_framework import serializers
from .models import Delivery, DeliveryStep, Return

class DeliveryStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStep
        fields = ['step', 'timestamp', 'location']

class DeliverySerializer(serializers.ModelSerializer):
    # Sérialisation des étapes (en lecture seule)
    steps = DeliveryStepSerializer(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = ['id', 'order_id', 'seller_id', 'delivery_man_id', 'customer_id', 'status', 'steps', 'created_at', 'updated_at']

class ReturnSerializer(serializers.ModelSerializer):
    # Sérialisation de l'objet Delivery (au lieu de juste son ID)
    delivery = DeliverySerializer(read_only=True)

    class Meta:
        model = Return
        fields = ['id', 'delivery', 'customer_id', 'reason', 'status', 'created_at', 'updated_at']
