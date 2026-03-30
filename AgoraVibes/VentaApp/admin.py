from django.contrib import admin
from .models import Venta
from django.http import HttpResponseRedirect
from django.urls import reverse

class VentaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'medio_pago')

    def response_add(self, request, obj, post_url_continue = None):
        url = reverse('admin:Detalle_VentaApp_detalleventa_add')
        return HttpResponseRedirect(f'{url}?venta={obj.id}')
    

admin.site.register(Venta, VentaAdmin)
