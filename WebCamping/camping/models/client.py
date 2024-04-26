from django.db import models
import uuid

class Client(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_city = models.CharField(max_length=200)
    client_country = models.CharField(max_length=200)
    