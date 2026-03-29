from django.contrib import admin
from .models import Producto
from django.utils.html import format_html


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "precio_unitario", "stock", "mostrar_imagen")
    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" />',
                obj.imagen.url
            )
        return "Sin imagen"

    mostrar_imagen.short_description = "Imagen"

    
admin.site.register(Producto, ProductoAdmin)

# Register your models here.

