from django.apps import AppConfig
import environ
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

class CampingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camping' 
    def ready(self):
        pass