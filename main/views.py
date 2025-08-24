from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hello, Django REST Framework is working from MAIN app!"})
