from django.db import models
# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_maxima = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    precio_boleta = models.IntegerField()
    imagen = models.ImageField(upload_to='EventoApp')

    class Meta:
        db_table = "evento"
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.nombre