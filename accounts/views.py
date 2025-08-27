# accounts/views.py
from django.http import JsonResponse

def accounts_api(request):
    return JsonResponse({"message": "Accounts API working!"})
