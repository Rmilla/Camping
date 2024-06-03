from django.db import models

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    nom_complet = models.CharField(max_length=200)
    id_ville = models.ForeignKey('client', on_delete=models.CASCADE, related_name='Client')