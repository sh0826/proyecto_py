
from django.db import models
from AgoraVibes import settings

# Create your models here.
class Reservacion(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    cantidad_personas= models.IntegerField(verbose_name='Cantidad de Personas')
    cantidad_mesas= models.IntegerField(verbose_name='Cantidad de Mesas')
    fecha_reservacion= models.DateField(verbose_name='Fecha de Reservación')
    ocasion= models.CharField(max_length=100, null=True, blank=True, verbose_name='Ocasión')

    def __str__(self):
        return f"Reservacion {self.user}"