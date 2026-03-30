
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class Venta(models.Model):
    MEDIOS_PAGO=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')
    medio_pago = models.CharField(max_length=20, choices=MEDIOS_PAGO, verbose_name='Medio de Pago')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total(self):
        total = sum(d.total for d in self.detalleventa_set.all())
        return total
    class Meta:
        verbose_name: 'Venta'
        verbose_name_plural = 'Ventas'
    def __str__(self):
        return f" Venta#{self.id} - {self.usuario}"
