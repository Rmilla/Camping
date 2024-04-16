from django.contrib import admin
from django_mongoengine import mongo_admin as admin
from camping.models import Camping, Flat

# Register your models here.
admin.site.register(Flat)
