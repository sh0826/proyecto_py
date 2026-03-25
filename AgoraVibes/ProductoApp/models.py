from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Producto (models.Model):
    TIPO_PRODUCTO = [
        ('licor', 'Licor'),
        ('cerveza', 'Cerveza'),
        ('cigarrillo', 'Cigarrillo'),
    ]
    UNIDAD_MD = [
        ('ml', "Ml"),
        ('l', "L"),
        ('paquete', 'Paquete'),
        ('medio', 'Medio'),
    ]
    nombre = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    cantidad_MD = models.IntegerField(null=True, blank=True)
    unidad_MD = models.CharField(max_length=8, choices=UNIDAD_MD, null=True, blank=True) 
    stock = models.IntegerField()
    precio_unitario = models.IntegerField()
    imagen = models.ImageField(upload_to="ProductoApp")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def clean(self):
        if self.unidad_MD and not self.cantidad_MD:
            raise ValidationError("Debe ingresar cantidad si hay unidad")
        if self.cantidad_MD and not self.unidad_MD:
            raise ValidationError("Debe ingresar unidad si hay cantidad")
        
    def __str__(self):
        if self.unidad_MD:
            return f"{self.nombre} - {self.cantidad_MD}{self.unidad_MD}" 
        else:
            return self.nombre
           