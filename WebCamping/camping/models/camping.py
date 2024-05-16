from django.db import models
import json
import os

json_file_path = 'C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack\\Camping\\WebCamping\\camping\\vehicle_emissions.json'
def donnees_vehicule():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
emissions = donnees_vehicule()
vehicules = [(key, key) for key in emissions.keys()]
print(vehicules)

class Camping(models.Model):
    #id = models.AutoField(primary_key=True)
    camping_name = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    camping_city = models.CharField(max_length=200)
    camping_country = models.CharField(max_length=200)
    id_adresse = models.ForeignKey('Adresse_camping', on_delete=models.CASCADE, related_name='camping')




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