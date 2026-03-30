from django.contrib import admin
from .models import Venta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    
    #def response_add(self, request, obj, post_url_continue = None):
        #url = reverse('admin:Detalle_VentaApp_detalleventa_add')
        #return HttpResponseRedirect(f'{url}?venta={obj.id}')

admin.site.register(Venta, VentaAdmin)
