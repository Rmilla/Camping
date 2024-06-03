from django.core.management.base import BaseCommand
import requests
import csv
import itertools
from django.db import connection

class Command(BaseCommand):      
    #API KEY AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk
    def add_arguments(self, parser):
        parser.add_argument("API_KEY", type=str, help="API Key for Google Maps")

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

    def read_csv_lines(self, csv_file_path, begin, end):
        with open(csv_file_path, "r", newline="", encoding="UTF-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            for _ in range(begin):
                next(reader)
            return list(itertools.islice(reader, end - begin))                                   )
    def handle(self, *args, **options):
        API_KEY = options["API_KEY"]

        #vehicle_emissions = self.load_vehicle_data()
        #Initialisation des dictionnaires pour trier les valeurs déjà entrées des autres valeurs
        vehicule_dict={}
        pays_dict={}
        ville_dict={}
        client_dict = {}
        camping_dict = {}
        distance_dict ={}
        voyage_dict={}
        #Initialisation des primary keys
        id_vehicule=1
        id_pays=1
        id_ville=1
        id_camping=1
        id_client=1
        id_distance=1
        id_voyage=1
        
        step = 100
        for line in range(0, 1000, step):
            part = self.read_csv_lines("MOCK_DATA.csv", line, line + step)
            for record in part:
                print("ID Voyage : ", id_voyage)
                #Insertion des véhicules dans la table camping_vehicule
                vehicule = record["Transport"]
                if vehicule=="Combustion engine car":
                    carac = ["Combustion engine car",0.218]
                elif vehicule=="Electric engine car":
                    carac = ["Electric engine car", 0.103]
                elif vehicule=="Train":
                    carac = ["Train", 0.003]
                else:
                    carac = ["Bus",0.113]
                if vehicule not in vehicule_dict.keys():
                    vehicule_dict[vehicule] = {"id" : id_vehicule, "vehicule": vehicule}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_vehicule VALUES (%s,%s,%s)",[id_vehicule, carac[0], carac[1]])
                        temp_id_vehicule= id_vehicule
                        id_vehicule = id_vehicule +1
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id_vehicule FROM camping_vehicule WHERE camping_vehicule.nom_vehicule =(%s)",[vehicule])
                        row = cursor.fetchone()
                        temp_id_vehicule = row[0]
                #Insertion des pays dans la table camping_pays
                pays = record["Country"]
                if pays not in pays_dict.keys():
                    pays_dict[pays] = {"id" : id_pays, "nom":pays}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_pays VALUES (%s,%s)",[id_pays, pays_dict[pays]["nom"]])
                        temp_id_pays = id_pays
                        id_pays = id_pays + 1
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id_pays FROM camping_pays WHERE camping_pays.nom = (%s)", [pays])
                        row = cursor.fetchone()
                        temp_id_pays = row[0]
                    
                #Insertion des villes dans la table camping_ville
                if record["City"].split(sep=" ")[0]=="Paris":
                    ville = "Paris"
                else:
                    ville = record["City"]
                if ville not in ville_dict.keys():
                     ville_dict[ville] = {"id" : id_ville, "nom": ville}
                     with connection.cursor() as cursor:
                          cursor.execute("INSERT INTO camping_ville VALUES (%s,%s,%s)", [id_ville, ville_dict[ville]["nom"],temp_id_pays])
                          temp_id_ville = id_ville
                          id_ville = id_ville + 1
                else:
                     with connection.cursor() as cursor:
                          cursor.execute("SELECT id_ville FROM camping_ville WHERE camping_ville.nom_ville = (%s)", [ville])
                          row = cursor.fetchone()
                          temp_id_ville = row[0]
                #Insertion des clients dans la table camping_client
                client = record["Name"]
                if client not in client_dict.keys():
                     client_dict[client] = {"id" : id_client, "nom":client}
                     with connection.cursor() as cursor:
                          cursor.execute("INSERT INTO camping_client VALUES (%s,%s,%s)", [id_client, client_dict[client]["nom"],temp_id_ville])
                          temp_id_client = id_client
                          id_client = id_client+1
                else:
                     with connection.cursor() as cursor:
                          cursor.execute("SELECT id_client FROM camping_client WHERE camping_client.nom_complet = (%s)", [client])
                          row = cursor.fetchone()
                          temp_id_client = row[0]
                #Insertion des campings dans la table camping_camping
                nom_camping, camping_adresse, ville_camping, country_camping = record["Camping"].split(sep="/") 
                camping_cp = camping_adresse[-6:-1]
                if nom_camping not in camping_dict.keys():
                     camping_dict[nom_camping] = {"id": id_camping, "nom":nom_camping}
                     with connection.cursor() as cursor:
                          cursor.execute("INSERT INTO camping_camping VALUES (%s,%s,%s,%s,%s,%s)",[id_camping, camping_dict[nom_camping]["nom"],camping_cp,camping_adresse,\
                                            ville_camping,
                                            country_camping
                                         ]
                                         )
                          temp_id_camping = id_camping
                          id_camping = id_camping +1
                else:
                     with connection.cursor() as cursor:
                          cursor.execute("SELECT id_camping FROM camping_camping WHERE camping_camping.nom_camping =(%s)", [nom_camping])
                          row = cursor.fetchone()
                          temp_id_camping = row[0]
                #Insertion des voyages dans la table camping_voyage
                date = record["Date"]
                if id_voyage not in voyage_dict.keys():
                    voyage_dict[id_voyage] = {"id": id_voyage}
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO camping_voyage VALUES (%s,%s,%s,%s,%s)",[id_voyage,date,temp_id_camping,temp_id_client,temp_id_vehicule
                                         ]
                                         )
                    id_voyage = id_voyage+1

                #Insertion des données dans la table distance
                API_KEY = "AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk"
                API_transport = "transit" if vehicule == "Train" else "driving"
                distance_sent = self.get_distance(API_KEY, ville_camping, ville, API_transport)
                if distance_sent == 'PROBLEM':
                    print("PROBLEM")
                    print("Ville client : ", ville)
                    print("Pays client : " , pays)
                    print("Vehicule : ", vehicule)
                    id_distance = id_distance+1
                    continue
                #Trie des valeurs selon qu'elles ont une virgule ou pas dans le retour de l'API distancemartix
                if "," in distance_sent:
                    distance = float(distance_sent.replace(",", ".")) * 1000
                else:
                    distance=float(distance_sent)
                distance = distance*2
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO camping_estdistant VALUES (%s,%s,%s,%s)",
                                           [
                                            id_distance,
                                            distance,
                                            temp_id_camping,
                                            temp_id_ville
                                           ]
                                           )
                    print("id distance : ", id_distance)
                    print("Ville camping : ", ville_camping)
                    print("Ville client : " , ville)
                    id_distance = id_distance+1
