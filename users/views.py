from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from cart.models import Cart, Product

class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginView(TokenObtainPairView):
    """Fusionner le panier de session avec celui en base de données"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = CustomUser.objects.get(email=request.data["email"])

            # Récuperer le panier en session
            session_cart = request.session.get("cart", {})

            for product_id, item in session_cart.item():
                product = Product.objects.get(id=product_id)

                # Vérifier si le produit est dejà dans le panier en DB
                cart_item, created = Cart.objects.get_or_create(user=user, product=product)
                if not created:
                    cart_item.quantity += item["quantity"]
                    cart_item.save()

            # Vider le panier session après fusion
            request.session["cart"] = {}
            request.session.modified = True

        return response
