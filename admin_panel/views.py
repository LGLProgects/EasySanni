# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from products.models import Notification 

# La vue de test
def test_view(request):
    return JsonResponse({'message': "L'Api fonctionne correctement"})
def notifications_view(request):
    """Vue pour afficher les notifications"""
    notifications = Notification.objects.filter(user=request.user)  # Filtrer les notifications pour l'utilisateur connecté
    return render(request, 'notifications.html', {'notifications': notifications})