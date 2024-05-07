from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserRole(models.TextChoices):
    ADMIN = 'AD' , 'Admin'
    USER = 'US' , 'User'

class LoginManager(BaseUserManager):
    """ Personnalisation de la gestion des utilisateurs afin d'intégrer la gestion de l'authentification par token"""
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("L'username est obligatoire.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class Login(AbstractBaseUser, PermissionsMixin):
    # Appliquer la gestion particulière de l'utilisateur au model customisé, qui hérite du model de django.
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(
        max_length=2,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    administrateur = models.BooleanField(default=False)
    objects = LoginManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


    def __str__(self):
        return self.username