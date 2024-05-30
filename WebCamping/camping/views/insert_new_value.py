from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework import status

from ..models import Client
from ..models import EstDistant
from ..models import Camping
from ..models import Ville
from ..models import voyage
from ..models import Voyage

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
        nom=request_data["client_fullname"]
        ville_client = request_data["client_city"]
        vehicule = request_data["vehicle"]
        camping = request_data["camping"]
        ville_camping = request_data["city_camping"]
        date = request_data["date"]
        pays = request_data["client_country"]

        #
        nom_filtre = Client.objects.filter(nom_complet__exact=nom)
        ville_filtre = Ville.objects.filter(nom_ville__exact=ville_client)
        date_filtre=Voyage.objects.filter(date__exact=date)
        print(nom_filtre)
        print(ville_filtre)
        print(date_filtre)
        if not ville_filtre.exists() or not nom_filtre.exists() or not date_filtre.exists():
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_pays FROM camping_pays WHERE camping_pays.nom = (%s)",
                               [pays]
                               )
                row = cursor.fetchone()
                id_pays = row[0]
                cursor.execute("SELECT id_vehicule FROM camping_vehicule WHERE camping_vehicule.nom_vehicule =(%s)",
                                   [vehicule]
                                   )
                row = cursor.fetchone()
                id_vehicule=row[0]
                cursor.execute("SELECT id_camping FROM camping_camping WHERE nom_camping =(%s)",
                                   [camping]
                                   )
                row = cursor.fetchone()
                id_camping = row[0]
                if not ville_filtre.exists():
                    cursor.execute("MAX(id_ville) FROM camping_ville")
                    row = cursor.fetchone()
                    id_ville = row[0]+1
                    cursor.execute("INSERT INTO camping_ville VALUES (%s,%s,%s)",
                                   [id_ville, ville_client, id_pays]
                                   )
                else:
                    cursor.execute("SELECT id_ville FROM camping_ville WHERE camping_ville.nom_ville = (%s)",
                                   [ville_client]
                                   )
                    row = cursor.fetchone()
                    id_ville = row[0]
                if not nom_filtre.exists():
                    cursor.execute("SELECT MAX(id_client) FROM camping_client")
                    row = cursor.fetchone()
                    id_client = row[0]+1
                    cursor.execute("INSERT INTO camping_client VALUES (%s,%s,%s)",
                                   [id_client, nom, id_ville]
                                   )
                else:
                    cursor.execute("SELECT id_client FROM camping_client WHERE camping_client.nom_complet =(%s)",
                                   [nom]
                                   )
                    row = cursor.fetchone()
                    id_client = row[0]
                if not date_filtre.exists():
                    cursor.execute("SELECT MAX(id_voyage) FROM camping_voyage")
                    row = cursor.fetchone()
                    id_voyage = row[0]+1
                    cursor.execute("INSERT INTO camping_voyage VALUES (%s,%s,%s,%s,%s)",
                                   [id_voyage, date, id_camping,id_client,id_vehicule]
                                   )
                API_KEY = "AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
                API_transport = "transit" if vehicule == "Train" else "driving"
                distance_sent = self.get_distance(API_KEY, ville_client, ville_camping, API_transport)
                if distance_sent == 'PROBLEM':
                    return Response({"message" : "Problème avec l'API de Google"}, status=status.HTTP_500_Internal_Server_Error)
                print(f"Distance_sent by API: {distance_sent}")
                #Trie des valeurs selon qu'elles ont une virgule ou pas dans le retour de l'API distancematrix
                if "," in distance_sent:
                    distance = float(distance_sent.replace(",", ".")) * 1000
                else:
                    distance=float(distance_sent)
                cursor.execute("SELECT MAX(id_distance) FROM camping_est")
                row = cursor.fetchone()
                id_distance = row[0]+1
                cursor.execute("INSERT INTO camping_estdistant VALUES (%s,%s,%s,%s)",
                               [id_distance, distance, id_camping, id_ville]
                               )
                
                
    # def post(self,request,*args,**kwargs):
        
    #     request_data=request.data
    #     vehicule = request_data['vehicle']
        
    #     with connection.cursor() as cursor:
    #                 cursor.execute(
    #     "SELECT MAX(id) FROM camping_client",
    #                 )
    #                 row = cursor.fetchone()
    #                 new_id_client = row[0]+1

    #     with connection.cursor() as cursor:
    #                 cursor.execute(
    #     "SELECT MAX(id) FROM camping_trip",
    #                 )
    #                 row = cursor.fetchone()
    #                 new_id_trip = row[0]+1

    #     self.create_client_and_trip(request_data,new_id_client, new_id_trip)
    #     return Response({"message" : "Client and trip created successfully."}, status=status.HTTP_201_CREATED)
    
    
    
    # def create_client_and_trip(self,request,new_id_client, new_id_trip):
    # # Create a new client
    #     new_client = Client.objects.create(
    #         id = new_id_client,
    #         client_city = request["client_city"],
    #         client_country = request["client_country"],
    # )
        
    #     API_KEY="AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
    #     with open('C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack4\\Camping\\WebCamping\\camping\\static\\vehicle_emissions.json', 'r') as file:
    #         vehicle_emissions = json.load(file)
    #     vehicle=request["vehicle"]
    #     unit_emissions = vehicle_emissions.get(vehicle)

    #     camping_instance = Camping.objects.get(camping_name=request["camping"])
        
    #     #distance_str=self.get_distance(API_KEY, request["client_city"], request["city_camping"], request["vehicle"])
    #     API_transport = "transit" if vehicle == "Train" else "driving"
    #     distance_sent = self.get_distance(API_KEY, request["client_city"], request["city_camping"], API_transport)
    #     if distance_sent == 'PROBLEM':
    #         return Response({"message" : "Problème avec l'API de Google"}, status=status.HTTP_500_Internal_Server_Error)
    #     print(f"Distance_sent by API: {distance_sent}")
    #     #Trie des valeurs selon qu'elles ont une virgule ou pas dans le retour de l'API distancematrix
    #     if "," in distance_sent:
    #         distance = float(distance_sent.replace(",", ".")) * 1000
    #     else:
    #         distance=float(distance_sent)
    #     #distance = float(distance_str[0])
    #     print("Distance : ",distance)
    # # Create a new trip associated with the newly created client
    #     new_trip = Trip.objects.create(
    #         id = new_id_trip,
    #         vehicle=vehicle,
    #         year=request["year"],
    #         distance = distance,
    #         emissions=distance*unit_emissions,
    #         client=new_client, # Associate the trip with the client
    #         camping = camping_instance
    # )
