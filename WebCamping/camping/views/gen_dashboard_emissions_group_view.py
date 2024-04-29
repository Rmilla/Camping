from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Camping, Client, Trip
from ..serializer import CampingSerializer, ClientSerializer, TripSerializer
from django.db.models import Prefetch

class NaturalJoinView(APIView):
    def get(self, request):
        # Prefetch related objects for Camping and Client
        campings = Camping.objects.prefetch_related(
            Prefetch('trip', queryset=Trip.objects.select_related('client'))
        )

        # Serialize the queryset
        serializer = CampingSerializer(campings, many=True)

        # Return the serialized data
        return Response(serializer.data)