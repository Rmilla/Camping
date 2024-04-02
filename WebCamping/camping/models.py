from django.db import models
from mongoengine import Document, fields
# Créations des modèles.

class Camping(Document):
    id_camping = fields.StringField(required=True, max_length=200)
    id_Adresses = fields.StringField(required=True, max_length=200)
    nom = fields.StringField(required=True, max_length=200)
    code_postale = fields.StringField(required=True)
    ville = fields.StringField(required=True)
    pays = fields.StringField(required=True)
    emission_total = fields.StringField(required=True)
    longitude = fields.StringField(required=True)
    latitude = fields.StringField(required=True)

class Adresses_campings(Document):
    id_Adresses = fields.StringField(required=True, max_length=200)
    Adresse_complète = fields.StringField(required=True, max_length=200)
    Pays = fields.StringField(required=True, max_length=200)

class Client(Document):
    id_client = fields.StringField(required=True, max_length=200)
    adress = fields.StringField(required=True, max_length=200)
    code_postal = fields.StringField(required=True, max_length=200)
    ville = fields.StringField(required=True, max_length=200)
    pays = fields.StringField(required=True, max_length=200)
    longitude = fields.StringField(required=True, max_length=200)
    latitude = fields.StringField(required=True, max_length=200)

class Voyager(Document):
    emission = fields.models.FloatField(required=True)
    vehicule = fields.StringField(required=True, choices=[('voiture','Voiture'),('avions','Avions'),('train','Train'),('moto','Moto'),('voitures_e','Voitures_electrique')], default='voiture')
    distance_parcourue = fields.models.FloatField(required=True)
    id_client = fields.StringField(required=True, max_length=200)
    id_camping = fields.StringField(required=True, max_length=200)


def calcul_emission(Voyager):
    # définis les facteurs d'émissions
    facteurs = {
        'voiture': 0.218,
        'moto': 0.191,
        'avions': 0.188,
        'voitures_e': 0.103,
        'train': 0.003
    }

    # vérifie si le vehicule est bien dans la liste des facteurs
    if Voyager.vehicule not in facteurs:
        raise ValueError(f"Vehicule type '{Voyager.vehicule}' is not supported.")

    # Calcule le taux d'émissions
    Voyager.emission = Voyager.distance_parcourue * facteurs[Voyager.vehicule]

    return Voyager.emission

print(f"The emission for a {Voyager.vehicule} traveling {Voyager.distance_parcourue} km is {Voyager.emission} kg of CO2.")