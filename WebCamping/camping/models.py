from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
import json
import os
# # Créations des modèles.
# json_file_path = os.path.join('C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack\\Camping\\WebCamping\\camping', 'vehicle_emissions.json')
# def donnees_vehicule():
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)
#     return data
# emissions = donnees_vehicule()
# vehicules = [tuple(emissions.keys())]
class Flat(Document):
    name_camping = fields.StringField(max_length=255)
    adress_camping = fields.StringField(max_length=255)
    city = fields.StringField(max_length=255)
    country_camping = fields.StringField(max_length=255)
    client_country = fields.StringField(max_length=255)
    client_city = fields.StringField(max_length=255)
    year = fields.IntField()
    transport_mode = fields.StringField(max_length=255)
    distance = fields.FloatField()
    emission_total = fields.DecimalField(max_digits=5, decimal_places=2)

json_file_path = 'C:/Projets/Stage/Camping/WebCamping/camping/vehicle_emissions.json'
def donnees_vehicule():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
emissions = donnees_vehicule()
vehicules = [set(emissions.keys())]
print(vehicules)

class Camping(Document):
    #id_camping = fields.StringField(rmax_length=200)
    camping_name = fields.StringField(max_length=200)
    #postal_code = fields.StringField()
    camping_city = fields.StringField(max_length=200)
    camping_country = fields.StringField(max_length=200)
    #emission_total = fields.StringField()

#class Adress_camping(Document):
    #id_Adresses = fields.StringField(max_length=200)
    #Adresse_complète = fields.StringField(max_length=200)
    #Pays = fields.StringField(max_length=200)

class Client(Document):
    #id_client = fields.StringField(max_length=200)
    #client_adress = fields.StringField(max_length=200)
    #code_postal = fields.StringField(max_length=200)
    client_city = fields.StringField(max_length=200)
    client_country = fields.StringField(max_length=200)

class Trip(Document):
    emissions = fields.FloatField()
    #vehicule = fields.StringField(choices=vehicules, default='voiture')
    vehicle = fields.StringField(max_length=200)
    distance = fields.FloatField()
    year = fields.IntField()


def calcul_emission(Voyager):
    # définis les facteurs d'émissions
    facteurs = donnees_vehicule()

    # vérifie si le vehicule est bien dans la liste des facteurs
    if Voyager.vehicule not in vehicules:
        raise ValueError(f"Vehicule type '{Voyager.vehicule}' is not supported.")

    # Calcule le taux d'émissions
    Voyager.emission = Voyager.distance_parcourue * facteurs[Voyager.vehicule]
    print(f"The emission for a {Voyager.vehicule} traveling {Voyager.distance_parcourue} km is {Voyager.emission} kg of CO2.")
    return Voyager.emission