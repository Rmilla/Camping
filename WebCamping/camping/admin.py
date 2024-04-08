from django.contrib import admin
from django_mongoengine import mongo_admin as admin
from .models import Camping, Adresses_campings, Client, Voyager
# Register your models here.

admin.site.register(Camping)
admin.site.register(Client)
admin.site.register(Adresses_campings)
admin.site.register(Voyager)
