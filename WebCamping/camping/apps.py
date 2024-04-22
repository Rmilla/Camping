from django.apps import AppConfig
import environ
from pathlib import Path
import os



class CampingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camping' 
    def ready(self):
        pass