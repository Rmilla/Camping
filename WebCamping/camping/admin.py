from django.contrib import admin
from django.urls import path

from .models.camping import Camping
from .models.client import Client
from .models.distance import EstDistant
from .models.pays import Pays
from .models.vehicule import Vehicule
from .models.ville import Ville
from .models.voyage import Voyage

# Register your models here.
admin.site.register(Camping)
admin.site.register(Client)
admin.site.register(EstDistant)
admin.site.register(Pays)
admin.site.register(Vehicule)
admin.site.register(Ville)
admin.site.register(Voyage)

