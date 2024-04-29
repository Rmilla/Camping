from django.core.management.base import BaseCommand
import requests
import csv
import itertools
from django.core.exceptions import MultipleObjectsReturned
import json
from camping.models.camping import Camping, Trip
from camping.models.client import Client
from camping.models.adresse import Adresse_camping

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
            print("data", data)
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

        step = 100
        for line in range(0, 1000, step):
            part = self.read_csv_lines("Fakedata.csv", line, line + step)
            for record in part:
                name_camping, camping_postal_adress, camping_city, country_camping = record["camping"].split(sep="/")
                print(camping_postal_adress)
                #camping_postal_code = camping_postal_adress.split("/")[1][-6:-1]
                country_client = record["Country"]
                city_client = record["City"].split(sep=" ")[0]
                year = record["Year"]
                transport = record["Transport"]

                API_transport = "transit" if transport == "Train" else "driving"

                distance = self.get_distance(API_KEY, city_client, camping_city, API_transport)
                if distance == 'PROBLEM':
                    continue
                distance = float(distance.replace(",", ".")) * 1000
                transport_em = vehicle_emissions.get(transport, 0)

                emission_total = transport_em * distance

                # self.create_flat_object(name_camping, camping_postal_adress, camping_city, country_camping, country_client, city_client, year, transport, distance, emission_total)
                self.create_adress_object(camping_postal_adress, country_camping,)
                adress_object = self.create_adress_object(camping_postal_adress, country_camping)
                self.create_camping_object(name_camping, camping_city, country_camping, adress_object)
                self.create_client_object(city_client, country_client)
                self.create_trip_object(emission_total, transport, distance, year, name_camping, city_client, country_client)
    #Path du fichier vehicle_emissions.json chez Pierre
    #"C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json"
    def load_vehicle_data(self):
        #json_file_path = os.path.join(os.path.dirname(__file__), 'vehicle_emissions.json')
        json_file_path ="C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json"
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def create_adress_object(self, camping_postal_adress, country_camping):
        adress_object = Adresse_camping(
            Adresse_complète = camping_postal_adress,
            Pays = country_camping,
        )
        adress_object.save()
        return adress_object
    def create_camping_object(self, name_camping, camping_city, country_camping, adress_object):
        camping_object = Camping(
            camping_name=name_camping,
            #postal_code = camping_postal_code,
            camping_city= camping_city,
            camping_country= country_camping,
            id_adresse = adress_object,
        )
        camping_object.save()

    def create_client_object(self, city_client, country_client):
        client_object = Client(
            client_city=city_client,
            client_country=country_client,
        )
        client_object.save()

    def create_trip_object(self, emission_total, transport, distance, year, camping_name, city_client, country_client):
        try:
            client_object, created = Client.objects.get_or_create(
            client_city=city_client,
            client_country=country_client,
        )
        except MultipleObjectsReturned:
            client_object = Client.objects.filter(
            client_city=city_client,
            client_country=country_client,
        ).first()
        created = False
        
        # client_object, created = Client.objects.get_or_create(
        #     client_city = city_client,
        #     client_country = country_client,
        # )
        
        camping_object = Camping.objects.filter(camping_name=camping_name).first()
        
        trip_object = Trip(
            emissions=emission_total,
            vehicle=transport,
            distance=distance,
            year=year,
            client= client_object,
            camping = camping_object
        )
        trip_object.save()

        # directions_result = gmaps.directions("Sydney Town Hall",
        #                                     "Parramatta, NSW",
        #                                     mode="driving",)
        # stock la distance dans une variable.
        # distance = directions_result[0]['legs'][0]['distance']['text']

    # def geolocalisation():
    #    city = 'london'
    #    api_url = 'https://api.api-ninjas.com/v1/geocoding?city='+city+''
    #    response = requests.get(api_url, headers={'X-Api-Key': '9ZhwyUW2uIaDzkXe5sdiYHPxJLGnahYLWNwA6UdX'})
    #    if response.status_code == requests.codes.ok:
    #        print(response.text)
    #    else:
    #        print("Error:", response.status_code, response.text)
    #    return response.text

    # def calculDistance():
    #    url = "https://api.myptv.com/routing/v1/routes?waypoints="+response.text["latitude"]+"&waypoints="+response.text["longitude"]+"&options[trafficMode]=AVERAGE"
    #    headers = {
    #        'apiKey': "RVVfNGUyN2U1NmU1M2U2NDM1NzhkODRjNGVmMjhmMmIxYzI6ZDNjMTc1ZmEtMTI0OS00OTk4LWJmN2QtMjk5M2I2YmU2ZGQy"
    #    }
    #    response = requests.request("GET", url, headers=headers)
    #    print(response.text.encode('utf8'))

    # geolocalisation()
    # calculDistance()