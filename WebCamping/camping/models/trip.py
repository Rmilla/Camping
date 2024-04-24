from django.db import models

class Trip(models.Model):
    emissions = models.FloatField()
    vehicle = models.CharField(choices=vehicules, default='voiture', max_length=200)
    distance = models.FloatField()
    year = models.IntegerField()
    client = models.ForeignKey('client', on_delete=models.CASCADE, related_name='trip')
    camping = models.ForeignKey('camping', on_delete=models.CASCADE, related_name='trip')