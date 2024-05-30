from django.db import models

class Ville(models.Model):
    id_ville = models.AutoField(primary_key=True)
    nom_ville = models.CharField(max_length=200)
    id_pays = models.ForeignKey('pays', on_delete=models.CASCADE, related_name='ville')