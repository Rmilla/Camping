from django.contrib import admin
from django_mongoengine import mongo_admin as admin
from Camping.WebCamping.camping.models.camping import Camping
from Camping.WebCamping.camping.models.camping import Trip
from Camping.WebCamping.camping.models.addresse import Adress_camping
from Camping.WebCamping.camping.models.client import Client



# Register your models here.
admin.site.register(Camping)
admin.site.register(Adress_camping)
admin.site.register(Client)
admin.site.register(Trip)
