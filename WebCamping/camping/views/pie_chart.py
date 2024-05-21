from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Camping, Client, Trip
from ..serializer import CampingSerializer, ClientSerializer, TripSerializer
from ..serializer import Pie_chart_serializer
from django.db import connection

class Pie_chart(APIView):
    def get(self, request):
        results={}
        print("Type de la requête : ", type(request.data), "Requête : ", request.data)
        year = request.data['year']
        print("Type de year : ", type(year), "Valeur de year : ", year)
        for camping in ["Belle Plage", "Blue Bayou", "Cap Sud", "València"]:
            with connection.cursor() as cursor:
                    cursor.execute("""SELECT SUM(ct.emissions) 
FROM camping_trip as ct
INNER JOIN camping_camping as cc ON cc.id = ct.camping_id 
WHERE ct.year = %s 
AND cc.camping_name = %s""",
                    [year, camping]
                    )
                    row = cursor.fetchone()
                    emissions = row[0]
                    results[camping]=emissions
                    print("Camping : ", camping, "Emissions : ", emissions)
        print(results)
        if connection.queries:
            last_query = connection.queries[-1]
            print("Last query: ", last_query['sql'])
        # Serialize the queryset
        corrected_results = {
        'belle_plage': results['Belle Plage'],
        'blue_bayou': results['Blue Bayou'],
        'cap_sud': results['Cap Sud'],
        'valencia': results['València']
                            }
        serializer = Pie_chart_serializer(data=corrected_results, many=False)
        print(serializer)
        # Return the serialized data
        if serializer.is_valid():
             return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)