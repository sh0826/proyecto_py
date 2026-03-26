
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Venta(models.Model):
    MEDIOS_PAGO=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    medio_pago = models.CharField(max_length=20, choices=MEDIOS_PAGO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
""" def total(self):
        total = sum(d.total for d in self.detalleventa_set.all())
        return total"""
def __str__(self):
        return f"Venta #{self.usuario}"

