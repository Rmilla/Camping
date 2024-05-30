from django.db import models

class Camping(models.Model):
    id_camping = models.AutoField(primary_key=True)
    nom_camping = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=200)
    adresse_complete = models.CharField(max_length=200)
    ville_camping = models.CharField(max_length=200)
    pays_camping = models.CharField(max_length=200)
    #id_ville = models.ForeignKey('ville', on_delete=models.CASCADE, related_name='camping')