from django.contrib import admin
from django.utils.html import mark_safe
from .models import Evento
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

# Register your models here.
class EventoResource(CustomExportResource):
    class Meta:
        model = Evento
        fields = (
            'nombre', 'capacidad_maxima', 'descripcion', 'fecha', 'hora_inicio', 'precio_boleta', 'mostrar_imagen'
        )


class EventoAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EventoResource
    list_display = ('nombre', 'capacidad_maxima', 'descripcion', 'fecha', 'hora_inicio', 'precio_boleta', 'mostrar_imagen')
    list_filter = ('nombre', 'fecha', 'precio_boleta', 'hora_inicio')
    readonly_fields = ('mostrar_imagen',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'

admin.site.register(Evento, EventoAdmin)