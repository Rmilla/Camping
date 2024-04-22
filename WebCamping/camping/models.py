from django.db import models
import json
# # Créations des modèles.

json_file_path = 'C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json'
def donnees_vehicule():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
emissions = donnees_vehicule()
vehicules = [set(emissions.keys())]
print(vehicules)

class Camping(models.Model):
    camping_name = models.CharField(max_length=200)
    postal_code = models.CharField()
    camping_city = models.CharField(max_length=200)
    camping_country = models.CharField(max_length=200)

class Adress_camping(models.Model):
    complete_adress = models.CharField(max_length=200)
    camping_country = models.CharField(max_length=200)

class Client(models.Model):
    client_adress = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    client_city = models.CharField(max_length=200)
    client_country = models.CharField(max_length=200)

class Trip(models.Model):
    
    emissions = models.FloatField()
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