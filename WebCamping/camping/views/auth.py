from django.shortcuts import render
from django.http import JsonResponse

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view, permission_classes


from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def printF(request):
    data={"response": "hello"}
    return JsonResponse(data)


class MyTokenObtainPairView(TokenObtainPairView):
    # Personnalisez la réponse pour inclure plus d'informations utilisateur si nécessaire
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Ajoutez des informations utilisateur supplémentaires à la réponse si nécessaire
        return response