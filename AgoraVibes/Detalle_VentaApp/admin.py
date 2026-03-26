
from django.contrib import admin
from .models import DetalleVenta

class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cant_prod', 'total_mostrado')

    def total_mostrado(self, obj):
        return obj.total

admin.site.register(DetalleVenta, DetalleVentaAdmin)
