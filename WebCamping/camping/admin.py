from django.contrib import admin
from django_mongoengine import mongo_admin as admin
from camping.models import Camping, Adress_camping, Client, Trip

# Register your models here.
admin.site.register(Camping)
admin.site.register(Adress_camping)
admin.site.register(Client)
admin.site.register(Trip)
