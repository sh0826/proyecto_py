from django.contrib import admin
from django.utils.html import mark_safe
from .models import Producto
from .forms import ProductoAdminForm
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from AgoraVibes.ExportResource import CustomExportResource

class ProductoResource(CustomExportResource):
    class Meta:
        model = Producto
        import_id_fields = ()
        fields = (
            'nombre',
            'tipo',
            'unidad_MD',
            'stock',
            'precio_unitario',
        )

class ProductoAdmin(ExportActionMixin, ImportExportModelAdmin ,admin.ModelAdmin):
    form = ProductoAdminForm
    resource_class = ProductoResource
    import_id_fields = ()
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
        'cantidad_MD',
        'precio_unitario',
    )
    search_fields = (        
        'nombre',
        'stock',
        'cantidad_MD',
        'precio_unitario',)
    search_help_text = "Nombre del producto, stock, cantidad de medida o precio unitario."
    
    readonly_fields = ('mostrar_imagen',)

    class Media:
        js = ('js/producto_admin.js',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'
    
admin.site.register(Producto, ProductoAdmin)
