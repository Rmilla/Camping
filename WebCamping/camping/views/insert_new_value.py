from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import requests
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework import status
from ..models import Client
from ..models import Trip
from ..models import Camping

class Insert_value(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_distance(self, api_key, start, end, mode):
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {"origins": start, "destinations": end, "mode": mode, "key": api_key}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()

            if data["status"] == "OK":
                if data["rows"][0]["elements"][0] in ({'status': 'NOT_FOUND'}, {'status': 'ZERO_RESULTS'}):
                    return "PROBLEM"
                else:
                    distance = data["rows"][0]["elements"][0]["distance"]["text"].split(" ")[0]
                    return distance
            else:
                print("Request failed.")
                print(response)
                return 'PROBLEM'
        else:
            print("Failed to make the request.")
            print(response)
            return 'PROBLEM'
#API KEY AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk
    

    def post(self,request,*args,**kwargs):
        
        request_data=request.data
        vehicle = request_data['vehicle']
        
        with connection.cursor() as cursor:
                    cursor.execute(
        "SELECT MAX(id) FROM camping_client",
                    )
                    row = cursor.fetchone()
                    new_id_client = row[0]+1

        with connection.cursor() as cursor:
                    cursor.execute(
        "SELECT MAX(id) FROM camping_trip",
                    )
                    row = cursor.fetchone()
                    new_id_trip = row[0]+1

        self.create_client_and_trip(request_data,new_id_client, new_id_trip)
        return Response({"message" : "Client and trip created successfully."}, status=status.HTTP_201_CREATED)
    
    
    
    def create_client_and_trip(self,request,new_id_client, new_id_trip):
    # Create a new client
        new_client = Client.objects.create(
            id = new_id_client,
            client_city = request["client_city"],
            client_country = request["client_country"],
    )
        
        API_KEY="AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
        with open('C:/Projets/Stage/Camping/WebCamping/camping/static/vehicle_emissions.json', 'r') as file:
            vehicle_emissions = json.load(file)
        vehicle=request["vehicle"]
        unit_emissions = vehicle_emissions.get(vehicle)

        camping_instance = Camping.objects.get(camping_name=request["camping"])
        
        #distance_str=self.get_distance(API_KEY, request["client_city"], request["city_camping"], request["vehicle"])
        API_transport = "transit" if vehicle == "Train" else "driving"
        distance_sent = self.get_distance(API_KEY, request["client_city"], request["city_camping"], API_transport)
        if distance_sent == 'PROBLEM':
            return Response({"message" : "Problème avec l'API de Google"}, status=status.HTTP_500_Internal_Server_Error)
        print(f"Distance_sent by API: {distance_sent}")
        #Trie des valeurs selon qu'elles ont une virgule ou pas dans le retour de l'API distancematrix
        if "," in distance_sent:
            distance = float(distance_sent.replace(",", ".")) * 1000
        else:
            distance=float(distance_sent)
        #distance = float(distance_str[0])
        print("Distance : ",distance)
    # Create a new trip associated with the newly created client
        new_trip = Trip.objects.create(
            id = new_id_trip,
            vehicle=vehicle,
            year=request["year"],
            distance = distance,
            emissions=distance*unit_emissions,
            client=new_client, # Associate the trip with the client
            camping = camping_instance
    )
