from django.contrib import admin
from .models import Reservacion
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

class ReservacionResourece(CustomExportResource):
    class Meta: 
        model = Reservacion
        fields = (
            'user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion'
        )

class ReservacionAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ReservacionResourece
    list_display = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    list_filter = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    search_fields = ('user__nombre_completo', 'ocasion')
    search_help_text = "Nombre del usuario o ocasión de la reserva."

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Reservacion, ReservacionAdmin)