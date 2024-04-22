from django.db import models
import json
import os

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    client_adress = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=200)
    client_city = models.CharField(max_length=200)
    client_country = models.CharField(max_length=200)