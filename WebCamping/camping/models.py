from django.db import models
import mongoengine
from mongoengine import Document, fields
# Créations des modèles.

class Camping(Document):
    id_camping = fields.StringField(rmax_length=200)
    id_Adresses = fields.StringField(max_length=200)
    nom = fields.StringField(max_length=200)
    code_postale = fields.StringField()
    ville = fields.StringField()
    pays = fields.StringField()
    emission_total = fields.StringField()
    longitude = fields.StringField()
    latitude = fields.StringField()

class Adresses_campings(Document):
    id_Adresses = fields.StringField(max_length=200)
    Adresse_complète = fields.StringField(max_length=200)
    Pays = fields.StringField(max_length=200)

class Client(Document):
    id_client = fields.StringField(max_length=200)
    adress = fields.StringField(max_length=200)
    code_postal = fields.StringField(max_length=200)
    ville = fields.StringField(max_length=200)
    pays = fields.StringField(max_length=200)
    longitude = fields.StringField(max_length=200)
    latitude = fields.StringField(max_length=200)

class Voyager(Document):
    emission = fields.FloatField()
    vehicule = fields.StringField(choices=[('voiture','Voiture'),('train','Train'),('bus','Bus'),('voitures_e','Voitures_electrique')], default='voiture')
    distance_parcourue = fields.FloatField()
    id_client = fields.StringField(max_length=200)
    id_camping = fields.StringField(max_length=200)
    année = fields.DateField()

def calcul_emission(Voyager):
    # définis les facteurs d'émissions
    facteurs = {
        'Voiture': 0.218,
        'Voitures_electrique': 0.103,
        'Train': 0.003,
        'Bus' : 0.113,
    }

    # vérifie si le vehicule est bien dans la liste des facteurs
    if Voyager.vehicule not in facteurs:
        raise ValueError(f"Vehicule type '{Voyager.vehicule}' is not supported.")

    # Calcule le taux d'émissions
    Voyager.emission = Voyager.distance_parcourue * facteurs[Voyager.vehicule]
    print(f"The emission for a {Voyager.vehicule} traveling {Voyager.distance_parcourue} km is {Voyager.emission} kg of CO2.")
    return Voyager.emission