from django.contrib import admin
from .models.camping import Camping
from .models.trip import Trip
from .models.adresse import Adresse_camping
from .models.client import Client
from .models.login import Login


# Register your models here.
admin.site.register(Camping)
admin.site.register(Adresse_camping)
admin.site.register(Client)
admin.site.register(Trip)