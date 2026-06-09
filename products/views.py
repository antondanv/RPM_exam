from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def health_check(requests):
    return JsonResponse({'status': 'ok'})
