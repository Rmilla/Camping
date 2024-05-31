from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializer import Distance_by_transport_Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import connection

class Distance_by_mean_of_transport(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results={}
        for year in range(2013,2024,1):
            for vehicle in ["Combustion engine car","Electric engine car", "Train","Bus"]:
                with connection.cursor() as cursor:
                    cursor.execute(
"SELECT SUM(ced.distance) \
FROM camping_vehicule as cve \
INNER JOIN camping_voyage as cvo ON cve.id_vehicule = cvo.id_vehicule_id \
INNER JOIN camping_camping as cac ON cvo.id_camping_id=cac.id_camping \
INNER JOIN camping_estdistant as ced ON ced.id_camping_id=cac.id_camping \
WHERE CAST(TO_CHAR(cvo.date, 'YYYY') AS INTEGER) = (%s) \
AND cve.nom_vehicule = %s",
                    [year,vehicle],
                    )
                    row = cursor.fetchone()
                    distance = row[0]
                    if vehicle not in results:
                        results[vehicle] = [] 
                    results[vehicle].append(distance)

        print("Results : " , results)
        #Serialize the queryset
        serializer_data = []
        for vehicle, distances in results.items():
            serializer = Distance_by_transport_Serializer(data={'vehicle': vehicle, 'distances': distances})
            if serializer.is_valid():
                serializer_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        print("Serializer data : ", serializer)
        # Return the serialized data
        return Response(serializer_data)