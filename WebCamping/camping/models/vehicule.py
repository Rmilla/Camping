from django.db import models

class Vehicule(models.Model):
    id_vehicule = models.AutoField(primary_key=True)
    nom_vehicule = models.CharField(max_length=200)
    empreinte_carbone_unitaire = models.FloatField()
