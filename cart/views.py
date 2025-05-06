from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Review
from .serializers import CartSerializer, CartItemSerializer, ReviewSerializer

# -----------------------
# Cart Views
# -----------------------

# Get current user's cart
class CartListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# Add a product to cart
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Update product quantity
class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=id, cart=cart)
        quantity = request.data.get('quantity')

        if quantity is None or int(quantity) < 1:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = int(quantity)
        cart_item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# Remove product from cart
class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=id, cart=cart)
        cart_item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# Clear entire cart
class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------
# Review Views
# -----------------------

# Get reviews for a product
class ProductReviewListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, productId):
        reviews = Review.objects.filter(product_id=productId)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


# Add a review
class AddReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update a review
class UpdateReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        review = get_object_or_404(Review, id=id, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = request.session.get('cart', {})
        return Response(cart)

    def post(self, request):
        product_id = str(request.data.get('product_id'))
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        request.session.modified = True
        return Response(cart, status=status.HTTP_201_CREATED)

    def put(self, request):
        product_id = str(request.data.get('product_id'))
        quantity = int(request.data.get('quantity', 1))

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] = quantity
            request.session['cart'] = cart
            request.session.modified = True
            return Response(cart)
        return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        product_id = str(request.data.get('product_id'))

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
            return Response(cart)
        return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)
class FusionnerPanierView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_cart = request.session.get('cart', {})

        if not session_cart:
            return Response({"message": "Le panier de session est vide."}, status=status.HTTP_204_NO_CONTENT)

        cart, created = Cart.objects.get_or_create(user=request.user)

        for product_id_str, quantity in session_cart.items():
            product_id = int(product_id_str)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product_id=product_id,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        # Nettoyer le panier session après fusion
        request.session['cart'] = {}
        request.session.modified = True

        serializer = CartSerializer(cart)
        return Response({
            "message": "Panier fusionné avec succès.",
            "panier_utilisateur": serializer.data
        }, status=status.HTTP_200_OK)

# Delete a review
class DeleteReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        review = get_object_or_404(Review, id=id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted"}, status=status.HTTP_204_NO_CONTENT)
