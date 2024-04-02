from django.apps import AppConfig
from mongoengine import connect
import environ
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

HOST=env("MONGODB_HOST")
PORT=env("MONGODB_PORT")
DATABASE="TestCamping"
PASSWORD=env("MONGODB_PASSWORD")
USERNAME=env("MONGODB_USERNAME")

#A voir si il faut vraiment rajouter le port (PORT) pour obtenir la connection
uri=f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
print(uri)

class CampingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camping'

"""    def ready(self):
        # Define the MongoDB connection settings
        # Connect to MongoDB
        connect(uri)"""
        
