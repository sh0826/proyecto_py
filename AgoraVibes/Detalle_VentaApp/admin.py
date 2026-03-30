
from django.contrib import admin
from .models import DetalleVenta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

class VentaResource(CustomExportResource):
    class Meta:
        model = DetalleVenta
        fields = ('venta', 'producto', 'cant_prod', 'total_mostrado')

class DetalleVentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = VentaResource
    list_display = ('producto', 'venta', 'cant_prod', 'total_mostrado')

    def total_mostrado(self, obj):
        return obj.total
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request) 
        venta_id = request.GET.get('venta')
        if venta_id:    
            initial['venta']= venta_id
        return initial

admin.site.register(DetalleVenta, DetalleVentaAdmin)
