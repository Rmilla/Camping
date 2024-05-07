from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from ..models import Camping, Client, Trip
from ..serializer import CampingSerializer, ClientSerializer, TripSerializer
from ..serializer import General_emission_group_serializer_years
from django.db import connection
from ..models.login import Login
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allow access only to Admin users.
    """
    def has_permission(self,request,view):
        user = request.user
        return user.role == Login.UserRole.ADMIN

class EmmissionGroup(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        
        if request.user.role == Login.UserRole.ADMIN:

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
        else:
            return Response({"message": "Accessible only by admins."})