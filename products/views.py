# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse

# La vue de test
def test_view(request):
    return JsonResponse({'message': "L'Api fonctionne correctement"})