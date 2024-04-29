from django.core.management.base import BaseCommand
import requests
import csv
import itertools
from django.core.exceptions import MultipleObjectsReturned
import json
from camping.models.camping import Camping
from camping.models.trip import Trip
from camping.models.client import Client
from camping.models.adresse import Adresse_camping
from django.db import connection
from django.db import IntegrityError

class Command(BaseCommand):
    # def __init__(self):
    #     self.connect_mongodb()

    # def connect_mongodb(self):
    #     if not mongoengine.connection._connections:
    #         mongoengine.connect(db="TestCamping", host=f"mongodb+srv://cluster0.l5yaw7u.mongodb.net/", username='camping', password="SqP6B8wLx62DsUf6", alias='default')
    #     else:
    #         mongoengine.connection.disconnect()
    #API KEY AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk
    def add_arguments(self, parser):
        parser.add_argument("API_KEY", type=str, help="API Key for Google Maps")

    def get_distance(self, api_key, start, end, mode):
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {"origins": start, "destinations": end, "mode": mode, "key": api_key}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            #print("data", data)
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

    def read_csv_lines(self, csv_file_path, begin, end):
        with open(csv_file_path, "r", newline="", encoding="ISO-8859-1") as file:
            reader = csv.DictReader(file, delimiter=";")
            for _ in range(begin):
                next(reader)
            return list(itertools.islice(reader, end - begin))
        
    

    def handle(self, *args, **options):
        API_KEY = options["API_KEY"]

        vehicle_emissions = self.load_vehicle_data()
        #Initialisation des dictionnaires pour trier les valeurs déjà entrées des autres valeurs
        ad_camping_dict={}
        client_dict={}
        camping_dict={}

        #Initialisation des primary keys
        id_adresse=1
        id_client=1
        id_camping=1
        id_trip=1

        step = 100
        for line in range(0, 1000, step):
            part = self.read_csv_lines("Fakedata.csv", line, line + step)
            for record in part:
                name_camping, camping_postal_adress, camping_city, country_camping = record["camping"].split(sep="/")
                camping_postal_code = camping_postal_adress[0][-6:-1]
                country_client = record["Country"]
                city_client = record["City"].split(sep=" ")[0]
                year = record["Year"]
                transport = record["Transport"]

                print('debut insetion ligne', line)
                #Insertion de chaque ligne dans la table Adresse_camping
                if name_camping not in ad_camping_dict.keys():
                    ad_camping_dict[name_camping] = {"id": id_adresse, "camping_postal_adress": camping_postal_adress, \
                                                  "camping_country": country_camping}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_adresse_camping VALUES (%s,%s,%s)", \
                            [
                             ad_camping_dict[name_camping]["id"],\
                             ad_camping_dict[name_camping]["camping_postal_adress"],\
                             ad_camping_dict[name_camping]["camping_country"]
                             ]
                                    )
                        temp_adresse = id_adresse
                        id_adresse=id_adresse+1
                        print(f"temp_adresse {temp_adresse}")
                        print(json.dumps(ad_camping_dict[name_camping],indent=4))

                #Insertion de chaque ligne dans la table Client (on considere que chaque ville est unique pour un pays donné)
                if city_client not in client_dict.keys():
                    client_dict[city_client] = {"id": id_client, "country_client": country_client, "city_client": city_client}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_client VALUES (%s,%s,%s)", \
                            [
                            client_dict[city_client]["id"],\
                            client_dict[city_client]["city_client"],\
                            client_dict[city_client]["country_client"]
                            ]       
                                       )
                        temp_id_client = client_dict[city_client]["id"]
                        id_client=id_client+1
                        print("if, temp_id_client", temp_id_client)
                else:
                    temp_id_client=client_dict[city_client]["id"]
                    print("else, temp_id_client", temp_id_client)
                #Insertion de chaque ligne dans la table Camping
                if name_camping not in camping_dict.keys():
                    camping_dict[name_camping] = {"id": id_camping, "name_camping": name_camping, "id_adresse": temp_adresse, \
                                                  "camping_postal_code": camping_postal_code, "camping_city": camping_city, \
                                                    "country_camping":country_camping}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_camping VALUES (%s,%s,%s,%s,%s,%s)",\
                            [
                            camping_dict[name_camping]["id"],
                            camping_dict[name_camping]["name_camping"],
                            camping_dict[name_camping]["camping_postal_code"],
                            camping_dict[name_camping]["camping_city"],
                            camping_dict[name_camping]["country_camping"],
                            camping_dict[name_camping]["id_adresse"]
                            ]           
                                       )
                        temp_id_camping=camping_dict[name_camping]["id"]
                        id_camping=id_camping+1
                        print("if, temp_id_camping", temp_id_camping)
                else:
                    temp_id_camping = camping_dict[name_camping]["id"]
                    print("else, temp_id_camping", temp_id_camping)
                #Insertion de chaque ligne dans la table trip
            
                API_transport = "transit" if transport == "Train" else "driving"
                distance = self.get_distance(API_KEY, city_client, camping_city, API_transport)
                if distance == 'PROBLEM':
                    continue
                distance = float(distance.replace(",", ".")) * 1000
                transport_em = vehicle_emissions.get(transport, 0)
                print(line, temp_id_client, temp_id_camping)
                emission_total = distance*transport_em
                
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO camping_trip (id, emissions, vehicle, distance, year, camping_id, client_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",\
                            [
                                id_trip,
                                emission_total,
                                transport,
                                distance,
                                year,
                                temp_id_camping,
                                temp_id_client,
                            
                            ]       
                                   )
                    id_trip=id_trip+1

    #Path du fichier vehicle_emissions.json chez Pierre
    #"C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json"
    def load_vehicle_data(self):
        #json_file_path = os.path.join(os.path.dirname(__file__), 'vehicle_emissions.json')
        json_file_path ="C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json"
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    
    