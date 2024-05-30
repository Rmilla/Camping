from django.db import models

class Pays(models.Model):
    id_pays = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    