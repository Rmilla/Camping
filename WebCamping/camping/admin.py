from django.contrib import admin
from django_mongoengine import mongo_admin as admin
from camping.models import Camping, Client, Flat, 

# Register your models here.
admin.site.register(Flat)
admin.site.register(Camping)
admin.site.register(Client)
