from django.db import models
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
class Flat(models.Model):
    name_camping = models.CharField(max_length=255)
    adress_camping = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country_camping = models.CharField(max_length=255)
    client_country = models.CharField(max_length=255)
    client_city = models.CharField(max_length=255)
    year = models.IntegerField()
    transport_mode = models.CharField(max_length=255)
    distance = models.FloatField()
    emission_total = models.DecimalField(max_digits=5, decimal_places=2)

json_file_path = 'C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json'
def donnees_vehicule():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
emissions = donnees_vehicule()
vehicules = [set(emissions.keys())]
print(vehicules)

class Camping(models.Model):
    #id_camping = fields.StringField(rmax_length=200)
    camping_name = models.CharField(max_length=200)
    #postal_code = fields.StringField()
    camping_city = models.CharField(max_length=200)
    camping_country = models.CharField(max_length=200)
    #emission_total = fields.StringField()

#class Adress_camping(Document):
    #id_Adresses = fields.StringField(max_length=200)
    #Adresse_complète = fields.StringField(max_length=200)
    #Pays = fields.StringField(max_length=200)

class Client(models.Model):
    #id_client = fields.StringField(max_length=200)
    #client_adress = fields.StringField(max_length=200)
    #code_postal = fields.StringField(max_length=200)
    client_city = models.CharField(max_length=200)
    client_country = models.CharField(max_length=200)

class Trip(models.Model):
    emissions = models.FloatField()
    #vehicule = fields.StringField(choices=vehicules, default='voiture')
    vehicle = models.CharField(max_length=200)
    distance = models.FloatField()
    year = models.IntegerField()


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