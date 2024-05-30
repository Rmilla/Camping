from django.db import models

class Voyage(models.Model):
    id_voyage = models.AutoField(primary_key=True)
    date = models.DateField()
    id_vehicule = models.ForeignKey('vehicule', on_delete=models.CASCADE,related_name='voyage')
    id_client = models.ForeignKey('client', on_delete=models.CASCADE, related_name='voyage')
    id_camping = models.ForeignKey('camping', on_delete=models.CASCADE, related_name='voyage')