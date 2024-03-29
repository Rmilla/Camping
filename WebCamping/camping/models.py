from django.db import models

# Create your models here.

class Camping(models.Model):
    id_camping = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)
    id_adresses = models.CharField(max_length=100)
    code_postal = models.IntegerField(default=34000, max_length=99999)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    emissions_total = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id_camping}'

class Client(models.Model):
    id_client = models.CharField(primary_key=True, max_length=100)
    adresse = models.CharField(max_length=100)
    code_postal = models.IntegerField(default=34000, max_length=99999)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id_client}'
    
class Adresse(models.Model):
    id_adresses = models.CharField(primary_key=True, max_length=100)
    adresse_complete = models.CharField(max_length=200)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id_adresses}'

class Manager_camping(models.Model):
    id_manager_camping = models.CharField(primary_key=True, max_length=100)
    administrateur = models.CharField(max_length=100)
