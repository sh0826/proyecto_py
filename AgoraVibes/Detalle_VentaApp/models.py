from django.contrib import admin
from django.db import models
from ProductoApp.models import Producto
from VentaApp.models import Venta   
from django.core.exceptions import ValidationError
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource


class DetalleVentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = CustomExportResource

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cant_prod = models.IntegerField(verbose_name='Cantidad de Producto')

    @property
    def total(self):
        return self.cant_prod * self.producto.precio_unitario

    class Meta:
        verbose_name = 'detalle venta'
        verbose_name_plural = 'detalles de ventas'

    def clean(self):
        if self.pk:
            detalleAnterior = DetalleVenta.objects.get(pk=self.pk)
            stock_real = self.producto.stock + detalleAnterior.cant_prod
        else:
            stock_real = self.producto.stock
        if self.cant_prod > stock_real:
            raise ValidationError("No hay suficiente cantidad del producto")

    def save(self, *args, **kwargs):
        if self.pk:
            detalleAnterior = DetalleVenta.objects.get(pk=self.pk)
            diferencia = self.cant_prod - detalleAnterior.cant_prod
            self.producto.stock -= diferencia
        else:
            self.producto.stock -= self.cant_prod

        self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto}"
 
