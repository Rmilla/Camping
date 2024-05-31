from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Camping, Client, EstDistant
from ..serializer import CampingSerializer, ClientSerializer, DistanceSerializer
from ..serializer import General_emission_group_serializer_years
from django.db import connection

class EmmissionGroup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results={}
        for year in range(2013,2024,1):
            with connection.cursor() as cursor:
                    cursor.execute(
"""SELECT SUM(cve.empreinte_carbone_unitaire*ced.distance) 
FROM camping_vehicule as cve
INNER JOIN camping_voyage as cvo ON cve.id_vehicule = cvo.id_vehicule_id
INNER JOIN camping_camping as cac ON cvo.id_camping_id=cac.id_camping
INNER JOIN camping_estdistant as ced ON ced.id_camping_id=cac.id_camping
WHERE CAST(TO_CHAR(cvo.date, 'YYYY') AS INTEGER) = %s """,
                    [year],
                    )
                    row = cursor.fetchone()
                    emissions = row[0]/1000
                    results[year]=emissions
        print(results)
        # Serialize the queryset
        serializer_data = []
        for year, emissions in results.items():
            serializer = General_emission_group_serializer_years(data={'year': year, 'emissions': emissions})
            if serializer.is_valid():
                print(serializer.data)
                serializer_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        print(serializer)
        # Return the serialized data
        return Response(serializer_data)