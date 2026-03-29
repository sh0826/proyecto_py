
from django.contrib import admin
from .models import DetalleVenta

class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cant_prod', 'total_mostrado')

    def total_mostrado(self, obj):
        return obj.total
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request) 
        venta_id = request.GET.get('venta')
        if venta_id:    
            initial['venta']= venta_id
        return initial

admin.site.register(DetalleVenta, DetalleVentaAdmin)
