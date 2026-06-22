
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Producto (models.Model):
    TIPO_PRODUCTO = [
        ('licor', 'Licor'),
        ('cerveza', 'Cerveza'),
        ('cigarrillo', 'Cigarrillo'),
    ]
    UNIDAD_MD = [
        ('ml', "Ml"),
        ('l', "Litros"),
        ('paquete', 'Paquete'),
        ('medio', 'Medio'),
    ]
    nombre = models.CharField(
        max_length=20,
        verbose_name='Nombre',
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
                message='El nombre solo puede contener letras y espacios.',
            )
        ],
    )
    tipo = models.CharField(verbose_name='Tipo', max_length=20, choices=TIPO_PRODUCTO)
    cantidad_MD = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Cantidad de Medida',
        validators=[MinValueValidator(0), MaxValueValidator(1500)],
    )
    unidad_MD = models.CharField(max_length=8, choices=UNIDAD_MD, null=True, blank=True, verbose_name='Unidad de Medida')
    stock = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
    )
    precio_unitario = models.IntegerField(
        verbose_name='Precio Unitario',
        validators=[MinValueValidator(0), MaxValueValidator(500000)],
    )
    imagen = models.ImageField(upload_to="ProductoApp", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        if self.cantidad_MD and self.unidad_MD:
            return f"{self.nombre} - {self.cantidad_MD}{self.unidad_MD}"
        return f"{self.nombre} - {self.unidad_MD}"   