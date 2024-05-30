from django.db import models

class EstDistant(models.Model):
    id_distance = models.AutoField(primary_key=True)
    distance = models.FloatField(default=None, null=True)
    id_ville = models.ForeignKey('ville', on_delete=models.CASCADE, related_name='distance')
    id_camping = models.ForeignKey('camping',on_delete=models.CASCADE,related_name='distance')