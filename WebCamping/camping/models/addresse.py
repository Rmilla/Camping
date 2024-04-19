from django.db import models
import json
import os

class Adress_camping(models.Model):
    id_Adresses = models.CharField(max_length=200)
    Adresse_complète = models.CharField(max_length=200)
    Pays = models.CharField(max_length=200)