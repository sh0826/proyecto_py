from django.contrib import admin
from django.utils.html import mark_safe
from .models import Producto
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

class ProductoResource(CustomExportResource):
    class Meta:
        model = Producto
        fields = (
            'nombre',
            'tipo',
            'cantidad_MD',
            'unidad_MD',
            'stock',
            'precio_unitario',
        )
class ProductoAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ProductoResource
    list_display = (
        'nombre',
        'tipo',
        'cantidad_MD',
        'unidad_MD',
        'stock',
        'precio_unitario',
        'mostrar_imagen'
    )

    list_filter = (
        'tipo',
        'unidad_MD',
        'cantidad_MD'
    )

    search_fields = (        
        'nombre',
        'cantidad_MD',
        'stock',
        'precio_unitario',)
    search_help_text = "Nombre del producto, cantidad, stock o precio unitario."
    
    readonly_fields = ('mostrar_imagen',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'
    
admin.site.register(Producto, ProductoAdmin)
