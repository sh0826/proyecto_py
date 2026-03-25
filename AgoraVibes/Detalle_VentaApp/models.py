from django.db import models
from django.contrib.auth.models import User
from ProductoApp.models import Producto
'''from VentaApp.models import Venta'''
from django.core.exceptions import ValidationError

class DetalleVenta(models.Model):
    '''MEDIO_PAGO = [
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ] va en venta
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cant_prod = models.IntegerField()
    medio_pago = models.CharField(max_length=20, choices=MEDIO_PAGO) va en venta
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'detalle venta'
        verbose_name_plural = 'detalles de ventas'

    def clean(self):
        if self.cant_prod > self.producto.stock:
            raise ValidationError("No hay suficiente cantidad del producto")
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.producto.stock -= self.cant_prod
            self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto}-{self.cant_prod}"
# Create your models here.
'''
