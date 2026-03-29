from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django import forms

# Create your models here.
class UsuarioManager(BaseUserManager):

    def crear_usuario(self, numero_documento, nombre_completo, correo, tipo, password=None):
        user = self.model(
            numero_documento=numero_documento,
            nombre_completo=nombre_completo,
            correo=self.normalize_email(correo),
            tipo=tipo,
        )
        user.set_password(password) # Esto cifra la contraseña (SHA256 por defecto)
        user.save(using=self._db)
        return user
    
    def crear_admin(self, numero_documento, nombre_completo, correo, tipo, password=None):
        user = self.crear_usuario(numero_documento, nombre_completo, correo, tipo, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, numero_documento, nombre_completo, correo, tipo, password=None):
        user = self.crear_usuario(numero_documento, nombre_completo, correo, tipo, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class FormularioLogeo (forms.Form):
    numero_documento = forms.IntegerField(label="Número de numero_documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class Usuario(AbstractUser):
    username = None
    
    TIPOS = (
        (1, 'Administrador'),
        (2, 'Empleado'),
        (3, 'Cliente'),
    )


    numero_documento = models.IntegerField(unique=True, primary_key=True, verbose_name='Número de Documento')
    tipo = models.IntegerField(default=3, choices=TIPOS, verbose_name='Tipo')
    nombre_completo = models.CharField(max_length=50)
    correo = models.EmailField(max_length=30)

    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'numero_documento'
    REQUIRED_FIELDS = ['nombre_completo', 'correo', 'tipo']

    def __str__(self):
        return self.nombre_completo or f"Usuario {self.numero_documento}"
    
    
class Recuperar(models.Model):
    correo = models.EmailField()
    token = models.CharField(max_length=64)

