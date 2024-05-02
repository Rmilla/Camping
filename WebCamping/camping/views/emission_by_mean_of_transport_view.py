from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializer import Emission_by_transport_Serializer
from django.db import connection

class Emissions_by_mean_of_transport(APIView):
    def get(self, request):
        results={}
        for year in range(2013,2024,1):
            for vehicle in ["Combustion engine car","Electric engine car", "Train","Bus"]:
                with connection.cursor() as cursor:
                    cursor.execute(
        "SELECT SUM(emissions) FROM camping_trip WHERE year = %s and vehicle = %s",
                    [year,vehicle],
                    )
                    row = cursor.fetchone()
                    emissions = row[0]
                    if vehicle not in results:
                        results[vehicle] = [] 
                    results[vehicle].append(emissions)

        print("Results : " , results)
        #Serialize the queryset
        serializer_data = []
        for vehicle, emissions in results.items():
            serializer = Emission_by_transport_Serializer(data={'vehicle': vehicle, 'emissions': emissions})
            if serializer.is_valid():
                serializer_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        print("Serializer data : ", serializer)
        # Return the serialized data
        return Response(serializer_data)