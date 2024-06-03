from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

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

        with connection.cursor() as cursor:
            cursor.execute("SELECT nom_complet FROM camping_client WHERE camping_client.nom_complet = (%s)", [nom])
            row = cursor.fetchone()
            print("Le nom en base est : ", row)
            if row == None:
                nom_filtre=True
            else:
                nom_filtre=False
            cursor.execute("SELECT nom_ville FROM camping_ville WHERE camping_ville.nom_ville = (%s)", [ville_client])
            row = cursor.fetchone()
            print("La ville en base est : ", row)
            if row == None:
                ville_filtre=True
            else:
                ville_filtre=False
            cursor.execute("SELECT date FROM camping_voyage WHERE camping_voyage.date =(%s)", [date]
                           )
            row = cursor.fetchone()
            print("La date en base est : ", row)
            if row == None:
                date_filtre=True
            else:
                date_filtre=False
        if ville_filtre or nom_filtre or date_filtre:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_pays FROM camping_pays WHERE camping_pays.nom = (%s)", [pays])                               
                row = cursor.fetchone()
                id_pays = row[0]
                cursor.execute("SELECT id_vehicule FROM camping_vehicule WHERE camping_vehicule.nom_vehicule =(%s)", [vehicule])
                row = cursor.fetchone()
                id_vehicule=row[0]
                cursor.execute("SELECT id_camping FROM camping_camping WHERE nom_camping =(%s)", [camping])
                row = cursor.fetchone()
                id_camping = row[0]
                if ville_filtre:
                    cursor.execute("SELECT MAX(id_ville) FROM camping_ville")
                    row = cursor.fetchone()
                    id_ville = row[0]+1
                    cursor.execute("INSERT INTO camping_ville VALUES (%s,%s,%s)", [id_ville, ville_client, id_pays])
                else:
                    cursor.execute("SELECT id_ville FROM camping_ville WHERE camping_ville.nom_ville = (%s)", [ville_client])
                    row = cursor.fetchone()
                    id_ville = row[0]
                if nom_filtre:
                    cursor.execute("SELECT MAX(id_client) FROM camping_client")
                    row = cursor.fetchone()
                    id_client = row[0]+1
                    cursor.execute("INSERT INTO camping_client VALUES (%s,%s,%s)", [id_client, nom, id_ville])
                else:
                    cursor.execute("SELECT id_client FROM camping_client WHERE camping_client.nom_complet =(%s)", [nom])
                    row = cursor.fetchone()
                    id_client = row[0]
                if date_filtre or nom_filtre or ville_filtre:
                    cursor.execute("SELECT MAX(id_voyage) FROM camping_voyage")
                    row = cursor.fetchone()
                    id_voyage = row[0]+1
                    cursor.execute("INSERT INTO camping_voyage VALUES (%s,%s,%s,%s,%s)",[id_voyage, date, id_camping,id_client,id_vehicule])
                API_KEY = "AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
                API_transport = "transit" if vehicule == "Train" else "driving"
                distance_sent = self.get_distance(API_KEY, ville_client, ville_camping, API_transport)
                if distance_sent == 'PROBLEM':
                    return Response({"message" : "Problème avec l'API de Google"}, status=status.HTTP_500_Internal_Server_Error)
                #Trie des valeurs selon qu'elles ont une virgule ou pas dans le retour de l'API distancematrix
                if "," in distance_sent:
                    distance = float(distance_sent.replace(",", ".")) * 1000
                else:
                    distance=float(distance_sent)
                distance= distance*2
                cursor.execute("SELECT MAX(id_distance) FROM camping_estdistant")
                row = cursor.fetchone()
                id_distance = row[0]+1
                cursor.execute("INSERT INTO camping_estdistant VALUES (%s,%s,%s,%s)",
                               [id_distance, distance, id_camping, id_ville]
                               )
                response = Response({"messsage": "Données ajoutées"}, status=status.HTTP_201_CREATED)
                return response
        else:
            response = Response({"message": "Voyage déjà dans la base"}, status=status.HTTP_401_UNAUTHORIZED)
            return response
