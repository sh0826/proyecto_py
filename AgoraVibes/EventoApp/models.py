from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from datetime import date
# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    capacidad_maxima = models.IntegerField(verbose_name='Capacidad Máxima', validators=[MaxValueValidator(40)])
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField(verbose_name='Fecha')
    hora_inicio = models.TimeField(verbose_name='Hora de Inicio')
    precio_boleta = models.IntegerField(verbose_name='Precio de Boleta')
    imagen = models.ImageField(upload_to='EventoApp')

    def cupos_disponibles(self):
        total = self.boleta_set.aggregate(
            total=Sum('cantidad_boletos')
        )['total'] or 0
        return self.capacidad_maxima - total

    def clean(self):
        if self.fecha < date.today():
            raise ValidationError("No puedes elegir fechas anterior a la de hoy ")

        mas_eventos = Evento.objects.filter(
            fecha=self.fecha
        ).exclude(
            pk=self.pk
        ).exists()

        if mas_eventos:
            raise ValidationError({
                'fecha':"No puede haber 2 eventos en un dia"
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = "evento"
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.nombre