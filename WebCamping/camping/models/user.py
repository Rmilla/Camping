from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import json
import os

class CustomUserManager(BaseUserManager):
    """ Personnalisation de la gestion des utilisateurs afin d'intégrer la gestion de l'authentification par token"""
    def create_user(self, email, origin_country, password, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, origin_country = origin_country, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Appliquer la gestion particulière de l'utilisateur au model customisé, qui hérite du model de django.
        email = models.EmailField(unique=True)
        is_active = models.BooleanField(default=True)
        first_name= models.CharField(max_length=30)
        last_name= models.CharField(max_length=30)
        origin_country = models.CharField(max_length=50)
        is_staff=models.BooleanField(default = False)
        is_superuser=models.BooleanField(default=False)