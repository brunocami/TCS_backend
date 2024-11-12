from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Manager personalizado para gestionar la creación de usuarios y superusuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico.")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        return self.create_user(email, first_name, last_name, password, is_staff=True, is_admin=True)



# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)  # Campo para verificar si es miembro del personal
    is_admin = models.BooleanField(default=False)  # Campo para verificar si es administrador
    is_active = models.BooleanField(default=True)  # Campo que indica si la cuenta está activa
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def is_user(self):
        return not self.is_admin