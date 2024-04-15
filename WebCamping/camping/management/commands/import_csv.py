from django.core.management.base import BaseCommand, CommandError
import requests
import googlemaps
import csv
import itertools
import mongoengine
from camping.models import Flat, Camping, Client, Trip


class Command(BaseCommand):
    mongoengine.connect(db="TestCamping", host=f"mongodb+srv://cluster0.l5yaw7u.mongodb.net/",
                    username='camping', password="SqP6B8wLx62DsUf6", alias='import')
    # remplir avec votre clé API Google Maps
    API_KEY = "AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
    # gmaps = googlemaps.Client(key='AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk')

    def add_arguments(self, parser):
        parser.add_argument("API_KEY", type=str, help="API Key for Google Maps")

    def get_dist(self, api_key, start, end, mode):
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {"origins": start, "destinations": end, "mode": mode, "key": api_key}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # print(f"Type des données renvoyées : {type(data)}")
            # print(f"Données brutes : {data}")
            if data["status"] == "OK":
                #print(data["rows"][0]["elements"][0])
                if data["rows"][0]["elements"][0] == {'status' : 'NOT_FOUND'} or data["rows"][0]["elements"][0] == {'status' : 'ZERO_RESULTS'}:
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

    csv_file_path = "Fakedata.csv"

    def handle(self, *args, **options):
        API_KEY = "AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"

        def read_line_csv(csv_file_path, begin, end):
            with open(csv_file_path, "r", newline="", encoding="ISO-8859-1") as file:
                reader = csv.DictReader(file, delimiter=";")
                for _ in range(begin):
                    next(reader)
                return list(itertools.islice(reader, end - begin))
        j=1
        for line in range(0, 903, 100):
            part = read_line_csv(self.csv_file_path, line, line + 100)
            for i in range(0, 100):
                print(f"Enregistrement {j}")
                j=j+1
                name_camping = part[i]["camping"].split(sep="/")[0]
                camping_postal_adress = part[i]["camping"].split(sep="/")[1]
                camping_city = part[i]["camping"].split(sep="/")[2]
                country_camping = part[i]["camping"].split(sep="/")[3]
                country_client = part[i]["Country"]
                city_client = part[i]["City"].split(sep=" ")[0]
                year = part[i]["Year"]
                if part[i]["Transport"] == "Train":
                    APItransport = "transit"
                    distance = self.get_dist(
                        API_KEY, city_client, camping_city, APItransport)
                    if distance == 'PROBLEM':
                        continue
                    elif "," in distance:
                        distance = float(distance.replace(",", "."))*1000
                    else:
                        distance = float(distance)
                    transport_em = 0.003
                    emission_total = transport_em * distance
                elif part[i]["Transport"] == "Electric engine car":
                    APItransport = "driving"
                    transport_em = 0.103
                    distance = self.get_dist(
                        API_KEY, city_client, camping_city, APItransport)
                    if distance == 'PROBLEM':
                        continue                
                    elif "," in distance:
                        distance = float(distance.replace(",", "."))*1000
                    else:
                        distance = float(distance)
                    emission_total = transport_em * distance
                elif part[i]["Transport"] == "Combustion engine car":
                    APItransport = "driving"
                    distance = self.get_dist(
                        API_KEY, city_client, camping_city, APItransport
                    )
                    if distance == 'PROBLEM':
                        continue
                    elif "," in distance:
                        distance = float(distance.replace(",", "."))*1000
                    else:
                        distance = float(distance)
                    transport_em = 0.218
                    emission_total = transport_em * distance
                else:
                    APItransport == "driving"
                    distance = self.get_dist(
                        API_KEY, city_client, camping_city, APItransport
                    )
                    if distance == 'PROBLEM':
                        continue
                    elif "," in distance:
                        distance = float(distance.replace(",", "."))*1000
                    else:
                        distance = float(distance)
                    transport_em = 0.113
                    emission_total = transport_em * distance
                print(f"Nom du camping : {name_camping}, Ville du camping : {camping_city}, Ville du client : {city_client}, Année : {year} , Mode de Transport : {part[i]['Transport']}")
                print(f"Distance : {distance}, Type de la distance : {type(distance)}")
                row_object = Flat(
                    name_camping=name_camping,
                    adress_camping=camping_postal_adress,
                    city=camping_city,
                    country_camping=country_camping,
                    client_country=country_client,
                    client_city=city_client,
                    year=year,
                    transport_mode=part[i]["Transport"],
                    distance=distance,
                    emission_total=emission_total,
                )
                row_object.save()
                
                camping_object = Camping(
                    camping_name = name_camping,
                    camping_city = camping_city,
                    camping_country = country_camping,
                )
                camping_object.save()
                client_object= Client(
                    client_city = city_client,
                    client_country = country_client,
                )                
                client_object.save()
                trip_object = Trip(
                    emissions = emission_total,
                    vehicle = part[i]["Transport"],
                    distance = distance,
                    year = year,
                )
                trip_object.save()
            mongoengine.disconnect(alias='import')    
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
