from django.db import models
import json

json_file_path = 'C:\\Users\\sabat\\Documents\\Diginamic\\Stage\\CampingBack2\\Camping\\WebCamping\\camping\\vehicle_emissions.json'
def donnees_vehicule():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
emissions = donnees_vehicule()
vehicules = [(key, key) for key in emissions.keys()]

class Trip(models.Model):
    emissions = models.FloatField(default=None, null=True)
    vehicle = models.CharField(choices=vehicules, default='Combustion engine car', max_length=200)
    distance = models.FloatField(default=None, null=True)
    year = models.IntegerField()
    client = models.ForeignKey('client', on_delete=models.CASCADE, related_name='trip')
    camping = models.ForeignKey('camping', on_delete=models.CASCADE, related_name='trip')