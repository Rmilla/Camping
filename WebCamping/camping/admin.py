from django.contrib import admin
from .models.camping import Camping
from .models.trip import Trip
from .models.adresse import Adresse_camping
from .models.client import Client
from django.urls import path
from camping.views.login_view import LoginView



# Register your models here.
admin.site.register(Camping)
admin.site.register(Adresse_camping)
admin.site.register(Client)
admin.site.register(Trip)
