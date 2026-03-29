
from django.contrib import admin
from .models import DetalleVenta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource


class DetalleVentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = CustomExportResource
    list_display = ('producto', 'cant_prod', 'total_mostrado')

    def total_mostrado(self, obj):
        return obj.total

admin.site.register(DetalleVenta, DetalleVentaAdmin)
