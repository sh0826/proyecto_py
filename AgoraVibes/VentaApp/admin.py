from django.contrib import admin
from .models import Venta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource
from Detalle_VentaApp.models import DetalleVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
class VentaResource (CustomExportResource):
    class Meta: 
        model = Venta
        fields = ('usuario', 'medio_pago', 'fecha')

class VentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = VentaResource

    inlines = [DetalleVentaInline]

    list_display = ('usuario', 'id', 'medio_pago', 'fecha', 'total')
    list_filter = ('usuario', 'medio_pago', 'fecha')
    search_fields = ('usuario__nombre_completo', 'usuario__numero_documento')
    search_help_text = "Nombre del usuario o por su número de documento."
    def total(self, obj):
        return obj.total
admin.site.register(Venta, VentaAdmin)
