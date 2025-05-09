from rest_framework import serializers
from .models import Vendor, Shop
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'phone_number', 'address', 'is_approved', 'created_at']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ['slug', 'created_at', 'updated_at']

class VendorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shop = ShopSerializer(source='shop', read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'phone_number', 'address', 'is_approved', 'shop', 'created_at']

class VendorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    shop_name = serializers.CharField(write_only=True)
    shop_description = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Vendor
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 
                 'address', 'shop_name', 'shop_description']

    def create(self, validated_data):
        # Création de l'utilisateur
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_vendor=True
        )
        
        # Création du vendeur
        vendor = Vendor.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            address=validated_data['address']
        )
        
        # Création de la boutique
        Shop.objects.create(
            vendor=vendor,
            name=validated_data['shop_name'],
            description=validated_data.get('shop_description', '')
        )
        
        return vendor