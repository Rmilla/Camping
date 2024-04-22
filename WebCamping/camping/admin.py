from django.contrib import admin
from .models.camping import Camping
from .models.camping import Trip
from .models.addresse import Adress_camping
from .models.client import Client



# Register your models here.
admin.site.register(Camping)
admin.site.register(Adress_camping)
admin.site.register(Client)
admin.site.register(Trip)
