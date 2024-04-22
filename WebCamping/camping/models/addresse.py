from django.db import models
import json
import os

class Adress_camping(models.Model):
    id = models.AutoField(primary_key=True)
    Adresse_complète = models.CharField(max_length=200)
    Pays = models.CharField(max_length=200)