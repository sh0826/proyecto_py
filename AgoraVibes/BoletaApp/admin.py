from django.contrib import admin
from .models import Boleta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

# Register your models here.
class BoletaResource(CustomExportResource):
    class Meta:
        model = Boleta
        fields = (
            'precio_boleta',
            'cantidad_boletos',
            'usuario',
            'evento__nombre',
        )

        export_order = (
            'usuario',
            'evento',
            'precio_boletos',
            'cantidad_boletos',
        )
class BoletaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = BoletaResource
    list_display = ('usuario', 'evento', 'cantidad_boletos', 'precio_boleta')
    search_fields = ('usuario__nombre_completo', 'evento__nombre')
    search_help_text = "Nombre del usuario o nombre del evento."

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False
    
    def has_search_permission(self, request):
        return True
    

admin.site.register(Boleta, BoletaAdmin)