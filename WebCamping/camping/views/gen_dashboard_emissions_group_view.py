from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Camping, Client, Trip
from ..serializer import CampingSerializer, ClientSerializer, TripSerializer
from ..serializer import General_emission_group_serializer_years
from django.db import connection

class EmmissionGroup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results={}
        for year in range(2013,2024,1):
            with connection.cursor() as cursor:
                    cursor.execute("SELECT SUM(emissions) FROM camping_trip WHERE year = (%s)",
                    [year],
                    )
                    row = cursor.fetchone()
                    emissions = row[0]
                    results[f'y{year}']=emissions
        print(results)
        # Serialize the queryset
        serializer = General_emission_group_serializer_years(data=results, many=False)
        print(serializer)
        # Return the serialized data
        if serializer.is_valid():
             return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)