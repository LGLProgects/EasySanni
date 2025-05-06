from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Delivery, DeliveryStep, Return
from .serializers import DeliverySerializer, ReturnSerializer


# Fonction utilitaire pour obtenir un objet ou renvoyer une erreur
def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Response({"error": f"{model.__name__} non trouvé"}, status=status.HTTP_404_NOT_FOUND)


# Récupérer toutes les livraisons
class DeliveryListView(APIView):
    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


# Suivre une livraison spécifique
class DeliveryDetailView(APIView):
    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk)
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)


# Assigner une livraison à un livreur
class DeliveryAssignView(APIView):
    def post(self, request, pk):
        delivery = get_object_or_404(Delivery, pk)
        delivery_man_id = request.data.get('delivery_man_id')
        
        if not delivery_man_id:
            return Response({"error": "delivery_man_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mise à jour de la livraison
        delivery.delivery_man_id = delivery_man_id
        delivery.status = 'attribue'
        delivery.save()

        # Ajouter l'étape de transfert vendeur
        DeliveryStep.objects.create(
            delivery=delivery,
            step='transfert_vendeur',
            location=request.data.get('location', '')
        )
        
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)


# Mettre à jour l'état d'une livraison
class DeliveryUpdateView(APIView):
    def put(self, request, pk):
        delivery = get_object_or_404(Delivery, pk)
        step = request.data.get('step')
        
        valid_steps = ['enlevement_par_un_livreur', 'client_recu']
        
        if step not in valid_steps:
            return Response({"error": "Étape invalide"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mise à jour du statut
        if step == 'enlevement_par_un_livreur':
            delivery.status = 'en_transi'
        elif step == 'client_recu':
            delivery.status = 'livres'
        
        delivery.save()

        # Ajouter l'étape correspondante
        DeliveryStep.objects.create(
            delivery=delivery,
            step=step,
            location=request.data.get('location', '')
        )
        
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)


# Demander un retour produit
class ReturnCreateView(APIView):
    def post(self, request):
        serializer = ReturnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vérifier le statut d'un retour
class ReturnDetailView(APIView):
    def get(self, request, pk):
        return_obj = get_object_or_404(Return, pk)
        serializer = ReturnSerializer(return_obj)
        return Response(serializer.data)
