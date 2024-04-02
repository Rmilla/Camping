from django.db import models
from mongoengine import Document, fields
# Create your models here.

class Camping(Document):
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
    adress = fields.StringField(required=True, max_length=200)
    code_postal = fields.StringField(required=True, max_length=200)
    ville = fields.StringField(required=True, max_length=200)
    pays = fields.StringField(required=True, max_length=200)
    longitude = fields.StringField(required=True, max_length=200)
    latitude = fields.StringField(required=True, max_length=200)

