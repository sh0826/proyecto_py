from django.contrib import admin
from .models import Venta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

class VentaResource (CustomExportResource):
    class Meta: 
        model = Venta
        fields = ('usuario', 'medio_pago', 'fecha')

class VentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = VentaResource
    list_display = ('usuario', 'medio_pago', 'fecha')
    list_filter = ('usuario', 'medio_pago', 'fecha')
    search_fields = ('usuario__nombre_completo', 'usuario__numero_documento')
    search_help_text = "Nombre del usuario o por su número de documento."

admin.site.register(Venta, VentaAdmin)
