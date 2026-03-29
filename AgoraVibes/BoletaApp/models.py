from django.db import models
from EventoApp.models import Evento
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Boleta(models.Model):
    precio_boleta = models.IntegerField(verbose_name='Precio de Boleta')
    cantidad_boletos = models.IntegerField(verbose_name='Cantidad de Boletos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        db_table = "boleta"
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"

    def __str__(self):
        return f"{self.usuario} / {self.evento}"